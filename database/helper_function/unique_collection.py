from deepdiff import DeepDiff
from pymongo import DESCENDING


from helper_function.filter_collection import fetch_bulk_data, add_list_to_documents


async def update_list_documents_asin(filter_x, datas, collection):
    """ Updadte list of documents
    """
    count = 0
    for filter in filter_x:
        for data in datas:
            if data.get('asin') == filter.get('asin'):
                diff = DeepDiff(data, filter)
                # diff = DeepDiff(data, filter)
                if diff:
                    # print(filter, '\n\n\n\n\n', data, '\n\n', diff)

                    collection.update_one({"asin": filter.get('asin')}, {"$set": filter})
                    count += 1
    return count



async def process_batch_and_update_collection(batch, second_collection):
    asin_list = [doc["asin"] for doc in batch]
    datas = await fetch_bulk_data(asin_list, second_collection, 'asin')
    filter_add = []
    filter_update = []


    # Check the asin field that not present in Database and add them
    asins_present = set(item['asin'] for item in datas)
    missing_asins = []
    remaining_asins = []

    for asin in asin_list:
        if asin not in asins_present:
            missing_asins.append(asin)
        else:
            remaining_asins.append(asin)

    if missing_asins:
        for item in batch:
            if item['asin'] in missing_asins:
                filter_add.append(item)

        await add_list_to_documents(filter_add, second_collection)
        print(f"added {len(filter_add)} to the database")

    if remaining_asins:
        print(f'Remaining asin: {len(remaining_asins)}')
        for item in batch:
            if item['asin'] in remaining_asins:
                filter_update.append(item)
        count = await update_list_documents_asin(filter_update, datas, second_collection)
        print(f"Updated {count} to the database")
    return None



async def create_indexes_if_not_exist(collection):
    """ Create index on query field
    """
    # Define index definitions
    await collection.create_index({'asin': DESCENDING })
    print("Index for asin")
    await collection.create_index({'seller_name': DESCENDING })
    print("Index for seller_name")
    await collection.create_index({'category': DESCENDING })
    print("Index for category")
    await collection.create_index({'roi_category': DESCENDING })
    print("Index for roi_category")
    await collection.create_index({'profit_uk': DESCENDING })
    print("Index for profit_uk")
    await collection.create_index({'supplier_code': DESCENDING })
    print("Index Created_6")
    await collection.create_index({'seller_price': DESCENDING })
    print("Index for supplier_code")
    await collection.create_index({'last_update_time': DESCENDING })
    print("Index for last_update_time")
    await collection.create_index({'sales_rank': DESCENDING})
    print("Index for sales_rank")
    

    await collection.create_index(
        [("brand", "text"), 
         ("category", "text"), 
         ("title", "text"), 
         ("amz_Title", "text")],
        name="text_index_for_search"
    )
    print("Search Index created for brand, category, title, amz_Title")
   
   

async def unique_asin(fetch_from, add_to):
    # Create indexes if they do not exist
    await create_indexes_if_not_exist(add_to)
    print("Index created successfully")
    
    limit = 10000  # Adjust as needed
    page = 1
    # Calculate total unique ASINs
    unique_asins = await fetch_from.distinct("asin")
    total_unique_asins = len(unique_asins)
    total_pages = -(-total_unique_asins // limit)  # Ceiling division to calculate total pages
    print(f"Total unique ASINs: {total_unique_asins}\nTotal pages: {total_pages}")

    while page <= total_pages:
        skip = (page - 1) * limit
        pipeline = [
            # Group by `asin` and find the document with the highest `profit_uk`
            {"$group": {
                "_id": "$asin",
                "maxProfit": {"$max": "$profit_uk"},
                "document": {"$first": "$$ROOT"}
            }},
            # Replace root with the document having the highest profit
            {"$replaceRoot": {"newRoot": "$document"}},
            # Sort by `asin` to ensure consistent pagination
            {"$sort": {"asin": 1}},
            # Skip and limit for pagination
            {"$skip": skip},
            {"$limit": limit},
            # Project to exclude unwanted fields
            {"$project": {"_id": 0, "ref_close": 0, "ref_down": 0, "ref_limit": 0, 'upc': 0, "ref_up": 0, 'csv_data': 0}}
        ]

        # Execute the aggregation pipeline
        cursor = fetch_from.aggregate(pipeline)
        batch = await cursor.to_list(length=None)
 
        if batch:
            await process_batch_and_update_collection(batch, add_to)

        page += 1
        print(f'PAGE: {page}')
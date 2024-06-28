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
                diff = DeepDiff(data, filter,  exclude_paths=['time_since_added'])
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
    print("Index Created_1")
    await collection.create_index({'seller_name': DESCENDING })
    print("Index Created_2")
    await collection.create_index({'category': DESCENDING })
    print("Index Created_3")
    await collection.create_index({'roi_category': DESCENDING })
    print("Index Created_4")
    await collection.create_index({'profit_uk': DESCENDING })
    print("Index Created_5")
    await collection.create_index({'supplier_code': DESCENDING })
    print("Index Created_6")
    await collection.create_index({'seller_price': DESCENDING })
    print("Index Created_7")
    await collection.create_index({'last_update_time': DESCENDING })
    print("Index Created_8")
    

    await collection.create_index(
        [("brand", "text"), 
         ("category", "text"), 
         ("title", "text"), 
         ("amz_Title", "text")],
        name="text_index_for_search"
    )
    print("Index Created_9")
   

async def unique_asin(fetch_from, add_to):
    await create_indexes_if_not_exist(add_to)
    print("Index created successfully")
    
    limit = 10000 # Adjust as needed
    page = 1
    total_documents = await fetch_from.estimated_document_count()


    total_pages = -(-total_documents // limit)  # Ceiling division to calculate total pages
    print(f"Total documents: {total_documents}\n Total_pages: {total_pages}")
 
    while page < total_pages:
        skip = (page - 1) * limit
        pipeline = [
            {"$group": {
                "_id": "$asin",
                "maxProfit": {"$max": "$profit_uk"},
                "document": {"$first": "$$ROOT"}
            }},
            {"$replaceRoot": {"newRoot": "$document"}},
            {"$sort": {"asin": 1}},  # Sort by `asin` to ensure consistent pagination
            {"$skip": skip},
            {"$limit": limit},
            {"$project": {"_id": 0, "ref_close": 0, "ref_down": 0, "ref_limit": 0, 'upc': 0, "ref_up": 0, 'csv_data': 0}}
        ]

        cursor = fetch_from.aggregate(pipeline)
        batch = await cursor.to_list(length=None)
 
        if batch:
            await process_batch_and_update_collection(batch, add_to)

        page += 1
        print(f'PAGE: {page}')
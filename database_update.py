from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import numpy as np
from deepdiff import DeepDiff
import re
from pymongo import DESCENDING, ASCENDING
from typing import List

username = 'fiverr_user'
password = 'fiverr_user'
gg_client = AsyncIOMotorClient(
    f"mongodb+srv://{username}:{password}@cluster0.sngd13i.mongodb.net/?retryWrites=true&w=majority",
    maxPoolSize=50,
)

mvp2 = gg_client["mvp2"]


    
def get_price(price_str):
    """ Convert string price to integer
    """
    if isinstance(price_str, str):
        match = re.search(r"(\d+\.\d+|\d+)", price_str)
        if match:
            return float(match.group())
    return None


async def fetch_bulk_data(asin: List[str], collection, column: str):
    """ Fetch list of documents based on list of supplier_code """
    
    # Perform an asynchronous find operation to get documents based on supplier_code
    cursor = collection.find(
        {column: {"$in": asin}},
        {"_id": 0}
    )
    
    # Await the cursor to get the documents list
    documents_list = await cursor.to_list(length=None)
    
    return documents_list


async def add_list_to_documents(documents, collection):
    """ Add list of documents to database
    """
    return collection.insert_many(documents)

async def update_list_documents_supplier(filter_x, datas, collection):
    """ Updadte list of documents
    """
    count = 0
    for filter in filter_x:
        for data in datas:
            if data.get('supplier_code') == filter.get('supplier_code'):
                diff = DeepDiff(data, filter,  exclude_paths=['time_since_added'])
                # diff = DeepDiff(data, filter)
                if diff:
                    print(filter, '\n\n\n\n\n', data, '\n\n', diff)

                    collection.update_one({"supplier_code": filter.get('supplier_code')}, {"$set": filter})
                    count += 1
    return count



async def update_list_documents_asin(filter_x, datas, collection):
    """ Updadte list of documents
    """
    count = 0
    for filter in filter_x:
        for data in datas:
            if data.get('asin') == filter.get('asin'):
                # diff = DeepDiff(data, filter,  exclude_paths=['time_since_added'])
                diff = DeepDiff(data, filter)
                if diff:
                    # print(filter, '\n\n\n\n\n', data, '\n\n', diff)

                    collection.update_one({"asin": filter.get('asin')}, {"$set": filter})
                    count += 1
    return count


async def create_or_update_filter_collection(items_list, collection):
    asin_list = []
    filter_add = []
    filter_update = []

    for item in items_list:
        asin_list.append(item.get('supplier_code'))

    # Fetch data base on the ASIN field
    datas = await fetch_bulk_data(asin_list, collection, 'supplier_code')

    # Check the supplier_code field that not present in Database and add them
    asins_present = set(item['supplier_code'] for item in datas)
    missing_asins = []
    remaining_asins = []

    for asin in asin_list:
        if asin not in asins_present:
            missing_asins.append(asin)
        else:
            remaining_asins.append(asin)

    if missing_asins:
        for item in items_list:
            if item['supplier_code'] in missing_asins:
                filter_add.append(item)

        await add_list_to_documents(filter_add, collection)
        print(f"added {len(filter_add)} to the database")

    if remaining_asins:
        for item in items_list:
            if item['supplier_code'] in remaining_asins:
                filter_update.append(item)
        count = await update_list_documents_supplier(filter_update, datas, collection)
        print(f"Updated {count} to the database")
    return None


# Function to fetch and save records
async def fetch_and_save_records(page: int, limit: int, fetch_from, add_to):
    skip = (page - 1) * limit

    pipeline = [
        {"$match": {"profit_uk": {"$gt": 1}}},  # Filter documents where profit_uk > 1
        {"$skip": skip},  # Skip documents based on the offset
        {"$limit": limit},  # Limit the number of documents returned
        {"$project":
            {"_id": 0, "ref_close": 0, "ref_down": 0, "ref_limit": 0,
            'upc': 0, "ref_up": 0, "supplier_discount": 0, "brand_discount": 0,
            "awaiting validation": 0, "FBA_fee": 0, "Reff_fees": 0, "Categories_Root": 0, "delivery": 0,
            "Pack": 0}}
    ]

    google_data_cursor = fetch_from.aggregate(pipeline)
    google_data =  await google_data_cursor.to_list(length=None)
   
    records_to_insert = [
        {k: get_price(v) if k == 'seller_price' else (v if not isinstance(v, float) or not np.isnan(v) else None) for k, v in item.items()}
        for item in google_data
    ]

    await create_or_update_filter_collection(records_to_insert, add_to)
    print("Done updating or adding")
   


"""
* Code for unique asin
"""

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








    # existing_documents = await second_collection.find({"asin": {"$in": asins}}).to_list(None)
    existing_documents_map = {doc["asin"]: doc for doc in existing_documents}

    for document in batch:
        asin = document["asin"]
        existing_document = existing_documents_map.get(asin)
        if existing_document:
            diff = DeepDiff(existing_document, document)
            if diff:
                await second_collection.replace_one({"asin": asin}, document)
                print("Document updated for ASIN:", asin)
            else:
                print("No changes detected for ASIN:", asin)
        else:
            await second_collection.insert_one(document)
            print("New document inserted for ASIN:", asin)



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

    await collection.create_index(
        [("brand", "text"), 
         ("category", "text"), 
         ("title", "text"), 
         ("amz_Title", "text")],
        name="text_index_for_search"
    )
    print("Index Created_8")
   


# async def unique_asin(fetch_from, add_to):
#     first_collection =  fetch_from
#     second_collection = add_to

#     await create_indexes_if_not_exist(add_to)
#     print("index created succesfully")
    
#     pipeline = [
#         {"$group": {
#             "_id": "$asin",  # Replace "uniqueField" with the actual name of your unique field
#             "maxProfit": {"$max": "$profit_uk"},  # Replace "profit_uk" with the actual name of your profit field
#             "document": {"$first": "$$ROOT"}
#         }},
#         {"$replaceRoot": {"newRoot": "$document"}}
#     ]

#     cursor = fetch_from.aggregate(pipeline)

#     batch_size = 5000  # Adjust as needed
#     batch = []
#     async for document in cursor:
#         batch.append(document)
#         if len(batch) == batch_size:
#             await process_batch_and_update_collection(batch, add_to)
#             batch = []

#     # Process any remaining documents in the last batch
#     if batch:
#         await process_batch_and_update_collection(batch, add_to)



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
            {"$limit": limit}
        ]

        cursor = fetch_from.aggregate(pipeline)
        batch = await cursor.to_list(length=None)
        if batch:
            await process_batch_and_update_collection(batch, add_to)

        page += 1
        print(f'PAGE: {page}')


async def main():
    mvp2_collection_lookup = mvp2["profit_supplier_lookup"]
    unique_collection_lookup = mvp2['unique_supplier_lookup']
    mvp2_collection = mvp2["cn_supplier_lookup"]


    page = 1
    limit = 10000 # Set your desired batch size
    # await unique_collection_lookup.drop()

    if 'profit_supplier_lookup' not in await mvp2.list_collection_names():
        await mvp2_collection_lookup.create_index({'supplier_code': DESCENDING })
        await mvp2_collection_lookup.create_index({'profit_uk': DESCENDING })
        await mvp2_collection_lookup.create_index({'asin': DESCENDING })
        print("New index created succesfully")

    print(await mvp2_collection_lookup.list_indexes()
    total_documents = await mvp2_collection.count_documents({"profit_uk": {"$gt": 1}})
    total_pages = -(-total_documents // limit)  # Ceiling division to calculate total pages
    print(f"Total documents: {total_documents}\n Total_pages: {total_pages}")
  
    while page <= total_pages:
        try:
            await fetch_and_save_records(page, limit, mvp2_collection, mvp2_collection_lookup)
            page+=1
            print(f'PAGE: {page}')
        except Exception as e:
            print(f"Error processing batch: {e}")


    await unique_asin(mvp2_collection_lookup, unique_collection_lookup)


if __name__ == "__main__":
    asyncio.run(main())
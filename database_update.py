from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import numpy as np
from deepdiff import DeepDiff
import re
from pymongo import DESCENDING, ASCENDING


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


async def fetch_bulk_data(asins, collection):
    """ Fetch list of documents based on list of ASINs """
    # Create an index on ASIN field for faster retrieval
    
    # Perform an asynchronous find operation to get documents based on ASINs
    cursor = collection.find(
        {"asin": {"$in": asins}},
        {"_id": 0}
    )
    
    # Await the cursor to get the documents list
    documents_list = await cursor.to_list(length=None)
    
    return documents_list


async def add_list_to_documents(documents, collection):
    """ Add list of documents to database
    """
    return collection.insert_many(documents)

async def update_list_documents(filter_x, datas, collection):
    """ Updadte list of documents
    """
    count = 0
    for filter in filter_x:
        for data in datas:
            if data.get('asin') == filter.get('asin'):
                diff = DeepDiff(data, filter,  exclude_paths=['time_since_added'])
                # diff = DeepDiff(data, filter)
                if diff:
                    collection.update_one({"ASIN": filter.get('ASIN')}, {"$set": filter})
                    count += 1
    return count

async def create_or_update_filter_collection(items_list, collection):
    asin_list = []
    records_to_insert = []
    filter_add = []
    filter_update = []

    for item in items_list:
        asin_list.append(item.get('asin'))

    # Fetch data base on the ASIN field
    datas = await fetch_bulk_data(asin_list, collection)

    # Check the ASIN field that not present in Database and add them
    asins_present = set(item['asin'] for item in datas)
    missing_asins = []
    remaining_asins = []

    for asin in asin_list:
        if asin not in asins_present:
            missing_asins.append(asin)
        else:
            remaining_asins.append(asin)

    if missing_asins:
        for item in items_list:
            if item['asin'] in missing_asins:
                filter_add.append(item)

        await add_list_to_documents(filter_add, collection)
        print(f"added {len(filter_add)} to the database")

    if remaining_asins:
        for item in items_list:
            if item['asin'] in remaining_asins:
                filter_update.append(item)
        count = await update_list_documents(filter_update, datas, collection)
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
   


async def main():
    mvp2_collection_lookup = mvp2["filter_supplier_lookup"]
    mvp2_collection = mvp2["supplier_lookup"]

    page = 1
    limit = 15000 # Set your desired batch size
  
    if 'filter_supplier_lookup' not in await mvp2.list_collection_names():
        await mvp2_collection_lookup.create_index({'title': DESCENDING })
        await mvp2_collection_lookup.create_index({'search_term': DESCENDING })
        await mvp2_collection_lookup.create_index({'amz_Title': DESCENDING })
        await mvp2_collection_lookup.create_index({'category': DESCENDING })
        await mvp2_collection_lookup.create_index({'brand': DESCENDING })
        await mvp2_collection_lookup.create_index({'roi_category': DESCENDING })
        await mvp2_collection_lookup.create_index({'profit_uk': DESCENDING })
        await mvp2_collection_lookup.create_index({'asin': DESCENDING })

    # print(await mvp2_collection_lookup.list_indexes()
    total_documents = await mvp2_collection.count_documents({"profit_uk": {"$gt": 1}})
    total_pages = -(-total_documents // limit)  # Ceiling division to calculate total pages
    print(f"Total documents: {total_documents}\n Total_pages: {total_pages}")
    while page <= total_pages:
        try:
            await fetch_and_save_records(page, limit, mvp2_collection, mvp2_collection_lookup)
            page+=1
        except Exception as e:
            print(f"Error processing batch: {e}")





async def create_highest_profit_collection():
    count = 0
    source_collection = mvp2["supplier_lookup"]
    pipeline = [
        # Group by 'asin' and find the document with the highest 'profit_uk' in each group
        {"$match": {"profit_uk": {"$gt": 1}}},
    ]

    async for document in source_collection.aggregate(pipeline):
        count += 1
        print(count)
        # await destination_collection_name.insert_one(document)





async def get_unique_asin_with_highest_profit(collection):
    skip = 0
    limit = 3

    pipeline = [
        {"$match": {"profit_uk": {"$gt": 1}}},  # Filter documents where profit_uk > 1
        {"$group": {
            "_id": "$asin",
            "highest_profit": {"$max": "$profit_uk"}
        }},
        
        {"$skip": skip},  # Skip documents based on the offset
        {"$limit": limit},  # Limit the number of documents returned
        {"$project":
            {"_id": 0, "ref_close": 0, "ref_down": 0, "ref_limit": 0,
            'upc': 0, "ref_up": 0, "supplier_discount": 0, "brand_discount": 0,
            "awaiting validation": 0, "FBA_fee": 0, "Reff_fees": 0, "Categories_Root": 0, "delivery": 0,
            "Pack": 0}}
    ]

    unique_asin_with_highest_profit = await collection.aggregate(pipeline).to_list(None)
    print(unique_asin_with_highest_profit)
    return unique_asin_with_highest_profit

if __name__ == "__main__":
    asyncio.run(main())
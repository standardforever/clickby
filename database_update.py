from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import numpy as np
from deepdiff import DeepDiff
import re


username = 'fiverr_user'
password = 'fiverr_user'
gg_client = AsyncIOMotorClient(
    f"mongodb+srv://{username}:{password}@cluster0.sngd13i.mongodb.net/?retryWrites=true&w=majority",
    maxPoolSize=50,
)

mvp2 = gg_client["mvp2"]


    
def get_price(price_str):
    if isinstance(price_str, str):
        match = re.search(r"(\d+\.\d+|\d+)", price_str)
        if match:
            return float(match.group())
    return None


async def fetch_bulk_data(asins, collection):
    """ Fetch list of documents based on list of ASINs """
    # Create an index on ASIN field for faster retrieval
    collection.create_index("asin")
    
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
    for filter in filter_x:
        for data in datas:
            if data.get('asin') == filter.get('asin'):
                diff = DeepDiff(data, filter,  exclude_paths=['time_since_added'])
                # diff = DeepDiff(data, filter)
                if diff:
                    collection.update_one({"ASIN": filter.get('ASIN')}, {"$set": filter})
    return ("updated")

async def create_or_update_filter_collection(items_list, collection):
    asin_list = []
    records_to_insert = []
    filter_add = []
    filter_update = []

    for item in items_list:
        asin_list.append(item.get('asin'))
        record = {k: v if not isinstance(v, float) or not np.isnan(v) else None for k, v in item.items()}
        record['seller_price'] = get_price(record["seller_price"])
        records_to_insert.append(record.copy())

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
            else:
                filter_update.append(item)
        await add_list_to_documents(filter_add, collection)
        print(f"added {len(filter_add)} to the database")
    if remaining_asins:
        print(await update_list_documents(filter_update, datas, collection))
    return "result"


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

    records_to_insert = [{k: v if not isinstance(v, float) or not np.isnan(v) else None for k, v in item.items()} for item in google_data]


    await create_or_update_filter_collection(records_to_insert, add_to)
    print("Done updating or adding")
   


async def main():
    mvp2_collection_lookup = mvp2["filter_supplier_lookup"]
    mvp2_collection = mvp2["supplier_lookup"]

    page = 1
    limit = 1000 # Set your desired batch size

    total_documents = await mvp2_collection.count_documents({})
    total_pages = -(-total_documents // limit)  # Ceiling division to calculate total pages
    while page <= total_pages:
        try:
            await fetch_and_save_records(page, limit, mvp2_collection, mvp2_collection_lookup)
            page+=1
            break
        except Exception as e:
            print(f"Error processing batch: {e}")

if __name__ == "__main__":
    asyncio.run(main())
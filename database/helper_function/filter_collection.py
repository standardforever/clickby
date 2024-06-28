import numpy as np
from deepdiff import DeepDiff
import re
from typing import List



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
                diff = DeepDiff(data, filter)
                # diff = DeepDiff(data, filter)
                if diff:
                    # print(filter, '\n\n\n\n\n', data, '\n\n', diff)

                    collection.update_one({"supplier_code": filter.get('supplier_code')}, {"$set": filter})
                    count += 1
    return count


async def create_or_update_filter_collection(items_list, collection):
    """ It sort the collection into two, the one to update and the new one to add
    """
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
    """ It fetch data from the main collection to and apply some filters
    """
    skip = (page - 1) * limit

    pipeline = [
        {"$match": {
            "profit_uk": {"$gt": 1},  # Filter documents where profit_uk > 1
            "sales_rank": {"$lt": 150000}  # Add filter for sales_rank < 150000
        }},
        {"$sort": {"profit_uk": 1}},
        {"$skip": skip},  # Skip documents based on the offset
        {"$limit": limit},  # Limit the number of documents returned
        {"$project":
            {"_id": 0, "ref_close": 0, "ref_down": 0, "ref_limit": 0,
            'upc': 0, "ref_up": 0, "supplier_discount": 0, "brand_discount": 0,
            "awaiting validation": 0, "FBA_fee": 0, "Reff_fees": 0, "Categories_Root": 0, "delivery": 0,
            "Pack": 0, "csv_data": 0}}
    ]

    google_data_cursor = fetch_from.aggregate(pipeline)
    google_data =  await google_data_cursor.to_list(length=None)
   
    records_to_insert = [
        {k: get_price(v) if k == 'seller_price' else (v if not isinstance(v, float) or not np.isnan(v) else None) for k, v in item.items()}
        for item in google_data
    ]

    await create_or_update_filter_collection(records_to_insert, add_to)
    print("Done updating or adding")
   
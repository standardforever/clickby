from fastapi import APIRouter, HTTPException, status
from typing import List
from app.utils import helper_function
from app.schemas.api_schema import FilterModel
import re
import numpy as np 
from main import app

router = APIRouter()


@router.get("/category")
async def get_categroy():
    category = await helper_function.get_unique_field(app.collection, 'category')
    return category

@router.get("/market")
async def get_market():
    market = await helper_function.get_unique_field(app.collection, 'marketplace_id')
    return market


@router.get('/supplier-name')
async def get_supplier_name():
    supplier_name = await helper_function.get_unique_field(app.collection, 'seller_name')
    return supplier_name

@router.get('/roi')
async def get_roi():
    roi = await helper_function.get_unique_field(app.collection, 'roi_category')
    return roi

@router.get('/store-price')
async def get_store_price():
    return [
         '<25%', '25-50', '50-100' 
    ]

@router.get('/filter')
async def filter_button():
    category = await helper_function.get_unique_field(app.collection, 'category')
    roi = await helper_function.get_unique_field(app.collection, 'roi_category')
    store_price = [
         '<25%', '25-50', '50-100' 
    ]
    supplier_name = await helper_function.get_unique_field(app.collection, 'seller_name')
    market = await helper_function.get_unique_field(app.collection, 'marketplace_id')
    return {
        'category': category,
        'roi': roi,
        'store_price': store_price,
        'supplier_name': supplier_name,
        'market': market,
    }


# Cache for product details
@router.get("/product/{asin}")
async def api_product_details(asin: str):
    items = await app.collection.find({"asin": asin}, {"_id": 0}).to_list(length=None)
    return items


import time
@router.post('/home/{limit}/{skip}') #, response_model=ResponseModel)
async def home(
    limit: int,
    skip: int,
    filter: FilterModel
):
    total_time = time.time()
    store_price_ranges = {"<25": (0, 25), "25-50": (25, 50), "50-100": (50, 100), "100>": 100}

    try:
        # Pipeline to filter documents based on profit_uk and apply pagination
        pipeline = [
            {"$sort": {"profit_uk": -1}},
            {"$skip": skip},  # Skip documents based on the offset
            {"$limit": limit},  # Limit the number of documents returned
            {"$project":
                {"_id": 0, "ref_close": 0, "ref_down": 0, "ref_limit": 0,
                'upc': 0, "ref_up": 0}}
        ]

        # Apply additional filters if provided
        query_params = {}

        if filter.search_term:
            regex_pattern = re.compile(filter.search_term, re.IGNORECASE)
            # Build the query for searching across all fields
            query_params["$or"] = [
                {"brand": {"$regex": regex_pattern}},
                {"category": {"$regex": regex_pattern}},
                {"title": {"$regex": regex_pattern}},
                {"seller_name": {"$regex": regex_pattern}},
                {"amz_Title": {"$regex": regex_pattern}},
            ]


        if filter.store_price in list(store_price_ranges):
            if filter.store_price != "100>":
                min_roi, max_roi = store_price_ranges[filter.store_price]
                roi_range = {"$gte": min_roi, "$lte": max_roi}
                query_params['seller_price'] = roi_range
            else:
                min_roi = store_price_ranges[filter.store_price]
                roi_range = {"$gte": min_roi}
                query_params['seller_price'] = roi_range

        # Sort_by ROI query Params
        if filter.roi:
            query_params['roi_category'] = {"$in": filter.roi}

        if filter.categories:
            query_params['category'] = {"$in": filter.categories}

        if filter.supplier_name:
            query_params['seller_name'] = {"$in": filter.supplier_name}

        if query_params:
            pipeline.insert(1, {"$match": query_params})  # Insert additional match stage after profit_uk filter

        # pipeline.append({"$sort": {"profit_uk": -1}})
        start_time = time.time()
        google_data_cursor =  app.collection.aggregate(pipeline)
        google_data = await google_data_cursor.to_list(length=None)

        # Record end time
        end_time = time.time()

        # Calculate query execution time
        execution_time = end_time - start_time

        # Print start and end times
        print("Query started at:", start_time)
        print("Query ended at:", end_time)
        print("Total execution time:", execution_time, "seconds")




        # total_count_time = time.time()
        total_count = await app.collection.estimated_document_count()
        # total_count_end_time = time.time()
        # execution_time_count = total_count_end_time - total_count_time
        # print("\n\n\n\n")
        # # Print start and end times
        # print("Query started at:", total_count_time)
        # print("Query ended at:", total_count_end_time)
        # print("Total execution time:", execution_time_count, "seconds")
        

        total_end_time = time.time()
        print(f"\n\nTotal time: {total_end_time - total_time}")
        return {
            "data": google_data,
            "total_count": total_count,
        }

    except Exception as e:
        print(e)
        return 500



# @router.post('/home/{limit}/{skip}') #, response_model=ResponseModel)
# async def home(
#     limit: int,
#     skip: int,
#     filter: FilterModel
# ):
#     store_price_ranges = {"<25": (0, 25), "25-50": (25, 50), "50-100": (50, 100), "100>": 100}

#     try:
#         # Pipeline to filter documents based on profit_uk and apply pagination
#         pipeline = [
#             {"$match": {"profit_uk": {"$gt": 1}}},  # Filter documents where profit_uk > 1
#             {"$project": {
#                 "_id": 0, 
#                 "ref_close": 0, 
#                 "ref_down": 0, 
#                 "ref_limit": 0,
#                 "upc": 0, 
#                 "ref_up": 0
#             }}
#         ]

#         # Apply additional filters if provided
#         query_params = {}

#         if filter.search_term:
#             regex_pattern = re.compile(filter.search_term, re.IGNORECASE)
#             # Build the query for searching across all fields
#             query_params["$or"] = [
#                 {"brand": {"$regex": regex_pattern}},
#                 {"category": {"$regex": regex_pattern}},
#                 {'search_term': {"$regex": regex_pattern}},
#                 {"title": {"$regex": regex_pattern}},
#                 {"seller_name": {"$regex": regex_pattern}},
#                 {"amz_Title": {"$regex": regex_pattern}},
#             ]

#         if filter.store_price in list(store_price_ranges):
#             if filter.store_price != "100>":
#                 min_roi, max_roi = store_price_ranges[filter.store_price]
#                 roi_range = {"$gte": min_roi, "$lte": max_roi}
#                 query_params['seller_price'] = roi_range
#             else:
#                 min_roi = store_price_ranges[filter.store_price]
#                 roi_range = {"$gte": min_roi}
#                 query_params['seller_price'] = roi_range

#         # Sort_by ROI query Params
#         if filter.roi:
#             query_params['roi_category'] = {"$in": filter.roi}

#         if filter.categories:
#             query_params['category'] = {"$in": filter.categories}

#         if filter.supplier_name:
#             query_params['seller_name'] = {"$in": filter.supplier_name}

#         if query_params:
#             pipeline.insert(1, {"$match": query_params})  # Additional match stage after profit_uk filter

#         # Add sort stage based on profit_uk (descending order for highest profit)
#         pipeline.append({"$sort": {"profit_uk": -1}})

#         # Add skip and limit stages for pagination
#         pipeline.append({"$skip": skip})
#         pipeline.append({"$limit": limit})

#         google_data_cursor =  app.collection.aggregate(pipeline)
#         google_data = await google_data_cursor.to_list(length=None)

#         total_count = await app.collection.count_documents(query_params)
        
#         return {
#             "data": google_data,
#             "total_count": total_count,
#         }

#     except Exception as e:
#         print(e)
#         return 500




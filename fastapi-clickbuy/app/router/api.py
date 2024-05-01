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
    return [
         '<25%', '25-50%', '50-100%' 
    ]

@router.get('/store-price')
async def get_store_price():
    return [
         '<25%', '25-50', '50-100' 
    ]



# @router.post('/home/{limit}/{skip}') #, response_model=ResponseModel)
# async def home(
#     limit: int,
#     skip: int,
#     filter: FilterModel
# ):
#     try:
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

#         if filter.categories:
#             query_params['category'] = {"$in": filter.categories}

#         if filter.supplier_name:
#             query_params['seller_name'] = {"$in": filter.supplier_name}

#         pipeline = [
#             {"$match": query_params},  # Match stage to filter documents
#             {"$skip": skip},  # Skip documents based on the offset
#             {"$limit": limit},  # Limit the number of documents returned
#              {"$project":
#                         {"_id": 0, "ref_close": 0, "ref_down": 0, "ref_limit": 0,
#                         'upc': 0, "ref_up": 0}}
#         ]
#         google_data_cursor =  app.collection.aggregate(pipeline)
#         google_data = await google_data_cursor.to_list(length=None)

#         google_data = [{k: v if not isinstance(v, float) or not np.isnan(v) else None for k, v in item.items()} for item in google_data]
#         # total_count = await app.collection.count_documents(query_params)
      
#         return {
#             "data": google_data,
#             "total_count": 200,
#         }


#     except Exception as e:
#         print(e)
#         return 'ol'





# from app.utils.database import connection
# @router.post('/home/{limit}/{skip}') #, response_model=ResponseModel)
# async def home(
#     limit: int,
#     skip: int,
#     filter: FilterModel
# ):
#     try:
#         # First stage of the pipeline to filter documents based on profit_uk
#         profit_stage = {"$match": {"profit_uk": {"$gt": 1}}}

#         # Second stage of the pipeline for the remaining filters and pagination
#         query_params = {"profit_uk": {"$gt": 1}}

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

#         if filter.categories:
#             query_params['category'] = {"$in": filter.categories}

#         if filter.supplier_name:
#             query_params['seller_name'] = {"$in": filter.supplier_name}

#         remaining_pipeline = [
#             {"$match": query_params},  # Match stage to filter documents based on remaining filters
#             {"$skip": skip},  # Skip documents based on the offset
#             {"$limit": limit},  # Limit the number of documents returned
#             {"$project":
#                 {"_id": 0, "ref_close": 0, "ref_down": 0, "ref_limit": 0,
#                 'upc': 0, "ref_up": 0}}
#         ]

#         # Merge the two stages of the pipeline
#         # pipeline = [profit_stage] + remaining_pipeline

#         # google_data_cursor =  app.collection.aggregate(pipeline)
#         # google_data = await google_data_cursor.to_list(length=None)

#         # google_data = [{k: v if not isinstance(v, float) or not np.isnan(v) else None for k, v in item.items()} for item in google_data]
#         print('done')
#         total_count = await app.collection.count_documents(query_params)
      
#         return {
#             "data": "google_data",
#             "total_count": total_count,
#         }

#     except Exception as e:
#         print(e)
#         return 'ol'





@router.post('/home/{limit}/{skip}') #, response_model=ResponseModel)
async def home(
    limit: int,
    skip: int,
    filter: FilterModel
):
    roi_ranges = {"<25": (0, 25), "25-50": (25, 50), "50-100": (50, 100)}
    store_price_ranges = {"<25": (0, 25), "25-50": (25, 50), "50-100": (50, 100), "100>": 100}
    uk_profit_ranges = {"1>": 1,"2>": 2, "3>": 3, "4>": 4, "5>": 5, "6>": 6, "7>": 7, "8>": 8, "9>": 9, "10>": 10}

    try:
        # Pipeline to filter documents based on profit_uk and apply pagination
        pipeline = [
            {"$match": {"profit_uk": {"$gt": 1}}},  # Filter documents where profit_uk > 1
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
                {'search_term': {"$regex": regex_pattern}},
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
        if filter.roi in list(roi_ranges):
            min_roi, max_roi = roi_ranges[filter.roi]
            roi_range = {"$gte": min_roi, "$lte": max_roi}
            query_params['roi_uk'] = roi_range


        if filter.categories:
            query_params['category'] = {"$in": filter.categories}

        if filter.supplier_name:
            query_params['seller_name'] = {"$in": filter.supplier_name}

        if query_params:
            pipeline.insert(1, {"$match": query_params})  # Insert additional match stage after profit_uk filter

        google_data_cursor =  app.collection.aggregate(pipeline)
        google_data = await google_data_cursor.to_list(length=None)

        # google_data = [{k: v if not isinstance(v, float) or not np.isnan(v) else None for k, v in item.items()} for item in google_data]
        total_count = await app.collection.count_documents(query_params)
        
        return {
            "data": google_data,
            "total_count": total_count,
        }

    except Exception as e:
        print(e)
        return 500

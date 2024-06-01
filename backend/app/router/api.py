from fastapi import APIRouter, HTTPException, status
from typing import List
from app.utils import helper_function
from app.schemas.api_schema import FilterModel
import re
import numpy as np 
from main import app
import traceback
import time
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
    items = await app.collection_profit.find({"asin": asin}, {"_id": 0, "csv_data": 0}).sort("profit_uk", -1).to_list(length=None)
    return items



# @router.post('/home/{limit}/{skip}')
# async def home(limit: int, skip: int, filter: FilterModel):
#     try:
#         total_count = 0
#         total_time = time.time()
#         store_price_ranges = {"<25": (0, 25), "25-50": (25, 50), "50-100": (50, 100), "100>": 100}

#         # Pipeline to filter documents based on profit_uk and apply pagination
#         pipeline = [
#             # {"$sort": {"profit_uk": -1}},
#             {"$skip": skip},  # Skip documents based on the offset
#             {"$limit": limit},  # Limit the number of documents returned
#             {"$project": {"_id": 0, "ref_close": 0, "ref_down": 0, "ref_limit": 0, 'upc': 0, "ref_up": 0}}
#         ]

#         # Apply additional filters if provided
#         if filter.search_term:
#             regex_pattern = re.compile(filter.search_term, re.IGNORECASE)
#             pipeline.insert(0, {"$match": {"$text": {"$search": filter.search_term}}})

#         if filter.store_price in store_price_ranges:
#             min_price, max_price = store_price_ranges[filter.store_price]
#             if filter.store_price != "100>":
#                 pipeline.insert(1, {"$match": {"seller_price": {"$gte": min_price, "$lte": max_price}}})
#             else:
#                 pipeline.insert(1, {"$match": {"seller_price": {"$gte": min_price}}})

#         if filter.roi:
#             pipeline.insert(1, {"$match": {"roi_category": {"$in": filter.roi}}})

#         if filter.categories:
#             pipeline.insert(1, {"$match": {"category": {"$in": filter.categories}}})

#         if filter.supplier_name:
#             pipeline.insert(1, {"$match": {"seller_name": {"$in": filter.supplier_name}}})

#         # Print pipeline
#         print("Pipeline:", pipeline)

#         # Execute the pipeline
#         start_time = time.time()
#         cursor = app.collection.aggregate(pipeline)
#         data = await cursor.to_list(length=None)
#         end_time = time.time()

#         # Calculate query execution time
#         execution_time = end_time - start_time
#         print("Total execution time:", execution_time, "seconds")

#         # Calculate total count
#         if not filter.search_term:
#             total_count = await app.collection.estimated_document_count()
#         else:
#             total_count = 500

#         total_end_time = time.time()
#         print("Total time:", total_end_time - total_time)

#         return {"data": data, "total_count": total_count}

#     except Exception as e:
#         traceback.print_exc()  # Print full traceback
#         return 500




@router.post('/count')
async def home(filter: FilterModel):
    try:
        total_time = time.time()
        store_price_ranges = {"<25": (0, 25), "25-50": (25, 50), "50-100": (50, 100), "100>": 100}

        # Build the match conditions
        match_conditions = {}

        if filter.search_term:
            match_conditions["$text"] = {"$search": filter.search_term}

        if filter.store_price in store_price_ranges:
            min_price, max_price = store_price_ranges[filter.store_price]
            if filter.store_price != "100>":
                match_conditions["seller_price"] = {"$gte": min_price, "$lte": max_price}
            else:
                match_conditions["seller_price"] = {"$gte": min_price}

        if filter.roi:
            match_conditions["roi_category"] = {"$in": filter.roi}

        if filter.categories:
            match_conditions["category"] = {"$in": filter.categories}

        if filter.supplier_name:
            match_conditions["seller_name"] = {"$in": filter.supplier_name}

        # Calculate total count
        if match_conditions:
            total_count = await app.collection.count_documents(match_conditions)

        else:
            total_count = await app.collection_profit.estimated_document_count()

        total_end_time = time.time()
        print("Total time:", total_end_time - total_time)

        return {"total_count": total_count, "total_time": total_end_time - total_time}

    except Exception as e:
        traceback.print_exc()  # Print full traceback
        return 500


@router.post('/home/{limit}/{skip}')
async def home(limit: int, skip: int, filter: FilterModel):
    try:
        total_time = time.time()
        store_price_ranges = {"<25": (0, 25), "25-50": (25, 50), "50-100": (50, 100), "100>": 100}

        # Pipeline to filter documents based on profit_uk and apply pagination
        pipeline = [
            {"$sort": {"profit_uk": -1}},
            {"$skip": skip},  # Skip documents based on the offset
            {"$limit": limit},  # Limit the number of documents returned
            {"$project": {"_id": 0, "ref_close": 0, "ref_down": 0, "ref_limit": 0, 'upc': 0, "ref_up": 0, 'csv_data': 0}}
        ]

        # Build the match conditions
        match_conditions = {}

        if filter.search_term:
            match_conditions["$text"] = {"$search": filter.search_term}

        if filter.store_price in store_price_ranges:
            min_price, max_price = store_price_ranges[filter.store_price]
            if filter.store_price != "100>":
                match_conditions["seller_price"] = {"$gte": min_price, "$lte": max_price}
            else:
                match_conditions["seller_price"] = {"$gte": min_price}

        if filter.roi:
            match_conditions["roi_category"] = {"$in": filter.roi}

        if filter.categories:
            match_conditions["category"] = {"$in": filter.categories}

        if filter.supplier_name:
            match_conditions["seller_name"] = {"$in": filter.supplier_name}

        # Add the match stage to the pipeline if there are any match conditions
        if match_conditions:
            pipeline.insert(0, {"$match": match_conditions})

        # Print pipeline
        print("Pipeline:", pipeline)

        # Execute the pipeline to retrieve data
        start_time = time.time()
        cursor = app.collection.aggregate(pipeline)
        data = await cursor.to_list(length=None)
        end_time = time.time()

        # Calculate query execution time
        execution_time = end_time - start_time
        print("Total execution time:", execution_time, "seconds")

        # Calculate total count
        if match_conditions:
            total_count = await app.collection.count_documents(match_conditions)
            # total_count = 50
        else:
            total_count = await app.collection_profit.estimated_document_count()
            

        total_end_time = time.time()
        print("Total time:", total_end_time - total_time)
       
        return {"data": data, "total_count": total_count, "total_time": total_end_time - total_time}

    except Exception as e:
        traceback.print_exc()  # Print full traceback
        return 500

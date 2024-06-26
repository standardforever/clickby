from fastapi import APIRouter, HTTPException, status
from typing import List
from app.utils import helper_function
from app.schemas.api_schema import FilterModel
import re
import numpy as np 
from main import app
import traceback
import time
from datetime import datetime, timedelta
router = APIRouter(tags=["Home"])


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

@router.get('/sales-rank')
async def get_sales_rank():
    return [
        "1 - 25k", "25 - 75k",
        "75k - 150k", "150k+"
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

        if (filter.start_date and filter.end_date) and (filter.start_date != filter.end_date):
            try:
                start_date = datetime.strptime(filter.start_date, "%Y-%m-%d %H:%M:%S")
                end_date = datetime.strptime(filter.end_date, "%Y-%m-%d %H:%M:%S")
                match_conditions['last_update_time'] = {
                    "$gte": start_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "$lt": (end_date + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
                }
                print("\n\n\n\n\nddfdefdfsfdsfdsfsdfdsfdsfds\n\n\n\n\n\n")
            except Exception as e:
                print(e)
                pass
        
        elif filter.start_date:
            try:
                start_date = datetime.strptime(filter.start_date, "%Y-%m-%d %H:%M:%S")
                match_conditions["last_update_time"] = {
                    "$gte": start_date.strftime("%Y-%m-%d %H:%M:%S")
                }
            except Exception as e:
                print(e)
                pass

        elif filter.end_date:
            try:
                end_date = datetime.strptime(filter.end_date, "%Y-%m-%d %H:%M:%S")
                match_conditions["last_update_time"] = {
                    "last_update_time": {
                        "$lt": (end_date + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
                    }
                }
            except Exception as e:
                print(e)
                pass

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


@router.post('/home')
async def home(filter: FilterModel, limit: int=50, skip: int=0, sort_by_column: str = "profit_uk", ascend_decend: int = -1,  count_doc: bool=False):
    try:
        total_time = time.time()
        store_price_ranges = {"<25": (0, 25), "25-50": (25, 50), "50-100": (50, 100), "100>": 100}
        sales_rank_ranges = {"1 - 25k": (1, 25000), "25k - 75k": (25000, 75000), "75k - 150k": (75000, 150000), "150k+": (150000, 0) } 

        # Pipeline to filter documents based on profit_uk and apply pagination
        pipeline = [
            {"$sort": {sort_by_column: ascend_decend}},
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

        if filter.sales_rank in sales_rank_ranges:
            min_price, max_price = sales_rank_ranges[filter.sales_rank]
            if filter.sales_rank != "150k+":
                match_conditions["sales_rank"] = {"$gte": min_price, "$lte": max_price}
            else:
                match_conditions["sales_rank"] = {"$gte": min_price}
        if filter.roi:
            match_conditions["roi_category"] = {"$in": filter.roi}

        if filter.categories:
            match_conditions["category"] = {"$in": filter.categories}

        if filter.supplier_name:
            match_conditions["seller_name"] = {"$in": filter.supplier_name}

        
        if (filter.start_date and filter.end_date):
            try:
                start_date = datetime.strptime(filter.start_date, "%Y-%m-%d %H:%M:%S")
                end_date = datetime.strptime(filter.end_date, "%Y-%m-%d %H:%M:%S")
                match_conditions['last_update_time'] = {
                    "$gte": start_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "$lt": (end_date + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
                }
                print("\n\n\n\n\nddfdefdfsfdsfdsfsdfdsfdsfds\n\n\n\n\n\n")
            except Exception as e:
                print(e)
                pass
        
        elif filter.start_date:
            try:
                start_date = datetime.strptime(filter.start_date, "%Y-%m-%d %H:%M:%S")
                match_conditions["last_update_time"] = {
                    "$gte": start_date.strftime("%Y-%m-%d %H:%M:%S")
                }
            except Exception as e:
                print(e)
                pass

        elif filter.end_date:
            try:
                end_date = datetime.strptime(filter.end_date, "%Y-%m-%d %H:%M:%S")
                match_conditions["last_update_time"] = {
                    "last_update_time": {
                        "$lt": (end_date + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
                    }
                }
            except Exception as e:
                print(e)
                pass

        
        # Add the match stage to the pipeline if there are any match conditions
        if match_conditions:
            pipeline.insert(0, {"$match": match_conditions})


        # Print pipeline
        print("Pipeline:", pipeline)


        # Execute the pipeline to retrieve data
        start_time = time.time()

        # Calculate total 
        total_count = 0
        if count_doc == True: 
            if match_conditions:
                total_count = await app.collection.count_documents(match_conditions)
            else:
                total_count = await app.collection_profit.estimated_document_count()

            return {"total_count": total_count}


        cursor = app.collection.aggregate(pipeline)
        data = await cursor.to_list(length=None)
        end_time = time.time()

        # Calculate query execution time
        execution_time = end_time - start_time
        print("Total execution time:", execution_time, "seconds")

                

        total_end_time = time.time()
        print("Total time:", total_end_time - total_time)
       
        return {"data": data, "total_count": total_count, "total_time": total_end_time - total_time}

    except Exception as e:
        traceback.print_exc()  # Print full traceback
        return 500

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
    return []
    market = await helper_function.get_unique_field(app.collection, 'marketplace_id')
    return market


@router.get('/supplier-name')
async def get_supplier_name():
    return []
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



@router.post('/home/{limit}/{skip}') #, response_model=ResponseModel)
async def home(
    limit: int,
    skip: int,
    filter: FilterModel
):
    try:
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

        if filter.categories:
            query_params['category'] = {"$in": filter.categories}

        if filter.supplier_name:
            query_params['seller_name'] = {"$in": filter.supplier_name}

        pipeline = [
            {"$match": query_params},  # Match stage to filter documents
            {"$skip": skip},  # Skip documents based on the offset
            {"$limit": limit},  # Limit the number of documents returned
             {"$project":
                        {"_id": 0, "ref_close": 0, "ref_down": 0, "ref_limit": 0,
                        'upc': 0, "ref_up": 0}}
        ]
        google_data_cursor =  app.collection.aggregate(pipeline)
        google_data = await google_data_cursor.to_list(length=None)

        google_data = [{k: v if not isinstance(v, float) or not np.isnan(v) else None for k, v in item.items()} for item in google_data]
        total_count = await app.collection.count_documents(query_params)
      
        return {
            "data": google_data,
            "total_count": total_count,
        }

    except Exception as e:
        print(e)
        return 'ol'
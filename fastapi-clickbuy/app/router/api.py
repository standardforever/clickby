from fastapi import APIRouter, HTTPException, status
import logging
from typing import List
from app.utils.database import filter
from app.utils import helper_function
from app.schemas import api_schema
import re

from typing import Optional

router = APIRouter()




router = APIRouter()
@router.get("/category")
async def get_categroy():
    category = await helper_function.get_unique_field(filter, 'Categories: Root')
    return category


@router.get('/supplier-name')
async def get_supplier_name():
    supplier_name = await helper_function.get_unique_field(filter, 'scraped_data.seller_name')
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


@router.get('/home')
async def home(
    skip: int = 0, limit: int = 40, roi_range: str = None, 
    store_price: str = None, supplier_name: str = None, category: str = None,
    search_term: str = None

):
    try:

        #=========================================================
        roi_ranges = {"<25": (0, 25), "25-50": (25, 50), "50-100": (50, 100)}
        store_price_ranges = {"<25": (0, 25), "25-50": (25, 50), "50-100": (50, 100), "100>": 100}
        uk_profit_ranges = {"1>": 1,"2>": 2, "3>": 3, "4>": 4, "5>": 5, "6>": 6, "7>": 7, "8>": 8, "9>": 9, "10>": 10}
        amazon_price_ranges = {"<25": (0, 25), "25-50": (25, 50), "50-100": (50, 100), "100>": 100}
        sales_rank_ranges = {"<10k": 10000, "<25k": 25000, "<40k": 40000, "40k>": 40000}

        query_params = {}

        # Store Price query params
        if store_price in store_price_ranges:
            if store_price != "100>":
                min_roi, max_roi = store_price_ranges[store_price]
                roi_range = {"$gte": min_roi, "$lte": max_roi}
                query_params['scraped_data.seller_price'] = roi_range
            else:
                min_roi = store_price_ranges[store_price]
                roi_range = {"$gte": min_roi}
                query_params['scraped_data.seller_price'] = roi_range

        # Sort_by ROI query Params
        if roi_range in roi_ranges:
            min_roi, max_roi = roi_ranges[roi_range]
            roi_range = {"$gte": min_roi, "$lte": max_roi}
            query_params['scraped_data.roi'] = roi_range

        # Category Price query Params
        if category:
            query_params['Categories: Root'] = category

        # Category Price query Params
        if supplier_name:
            query_params['scraped_data.seller_name'] = supplier_name


        pipeline = [
                    {"$match": query_params},  # Match stage to filter documents
                    {"$skip": skip},  # Skip documents based on the offset
                    {"$limit": limit},  # Limit the number of documents returned
                    {"$project": {"_id": 0}}
                ]
        
        print(pipeline)
        
        google_data_cursor =  filter.aggregate(pipeline)
        google_data = await google_data_cursor.to_list(length=None)

        total_count = await filter.count_documents(query_params)
        
        return {
            "data": google_data,
            "total_count": total_count,
        }
    except Exception as e:
        print(e)
        return 'ol'



@router.get('/search')
async def search(search_term: str = None, skip: int = 0, limit: int = 40):
    try:
        query_params = {}
        if search_term:
            regex_pattern = re.compile(search_term, re.IGNORECASE)
            # Build the query for searching across all fields
            query_params = {
                "$or": [
                    {"Brand": {"$regex": regex_pattern}},
                    {"Categories: Root": {"$regex": regex_pattern}},
                    {'search_term': {"$regex": regex_pattern}},
                    {"Title": {"$regex": regex_pattern}},
                    {"URL: Amazon": {"$regex": regex_pattern}},
                    {"scraped_data.seller_name": {"$regex": regex_pattern}},
                    {"scraped_data.product_link": {"$regex": regex_pattern}},
                    {"scraped_data.seller_price": {"$regex": regex_pattern}},
                    {"scraped_data.profit": {"$regex": regex_pattern}},
                    {"scraped_data.roi": {"$regex": regex_pattern}},
                    {"scraped_data.roi_category": {"$regex": regex_pattern}},
                ]
            }

        pipeline = [
                    {"$match": query_params},  # Match stage to filter documents
                    {"$skip": skip},  # Skip documents based on the offset
                    {"$limit": limit},  # Limit the number of documents returned
                    {"$project": {"_id": 0}}
                ]
            
        google_data_cursor =  filter.aggregate(pipeline)
        google_data = await google_data_cursor.to_list(length=None)

        total_count = await filter.count_documents(query_params)
            
        return {
            "data": google_data,
            "total_count": total_count,
        }
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error'
        )


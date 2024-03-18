from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from app.utils.database import filter
from app.router import api

app = FastAPI()


@app.on_event("startup")
async def startup_events():
    await filter.create_index("scraped_data.roi_category")
    await filter.create_index("Categories: Root")
    await filter.create_index("scraped_data.seller_name")
    await filter.create_index("Amazon Price")
    await filter.create_index("last_update_time")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(api.router,
                    tags=['ClickByApi'],
                    prefix='/api/v1')

@app.get('/')
async def root():
    return {"Message": "Welcome to clickby Api with FastApi"}




# @app.get('/home')
# async def home():
#     # unique_categories = filter.distinct("Categories: Root")
#     # unique_supplier_name = filter.distinct("scraped_data.seller_name")
#     # unique_market_place = filter.distinct("search_term")
#     unique_date_added = filter.distinct("last_update_time")
#     print(unique_date_added)
#     return {
#         # "unique_categories": unique_categories,
#         # "unique_supplier_name": unique_supplier_name,
#         # "unique_market_place": unique_market_place,
#         "unique_date_added": unique_date_added
#     }



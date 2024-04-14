# from pymongo import MongoClient

# # Local MongoDB connection
# local_client = MongoClient(f'mongodb://admin:supersecret@localhost:27017')
# local_db = local_client["local_db"]  # Change "local_db" to your desired local database name
# local_collection = local_db["supplier_lookup"]  # Collection name in local database

# # MongoDB Atlas connection
# username = 'fiverr_user'
# password = 'fiverr_user'
# gg_client = MongoClient(
#     f"mongodb+srv://{username}:{password}@cluster0.sngd13i.mongodb.net/?retryWrites=true&w=majority",
#     maxPoolSize=50,
# )
# mvp2 = gg_client["mvp2"]
# mvp2_collection = mvp2["supplier_lookup"]

# # Function to fetch and save records
# def fetch_and_save_records():
#     # Retrieve the first 100 records
#     skip = 0
#     limit = 2000
#     for i in range(20):
#         cursor = mvp2_collection.find().skip(skip).limit(limit)

#         # Insert all records into the local database
#         records_to_insert = list(cursor)
#         if records_to_insert:
#             local_collection.insert_many(records_to_insert)
#             print("Records saved to local database successfully!")
#         else:
#             print("No records found to save.")
#         skip += 2000

# # Call the function to fetch and save records
# fetch_and_save_records()


from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()


# Retrieve environment variables
# username = quote_plus(os.getenv("MONGO_USER"))
# password = quote_plus(os.getenv("MONGO_PASS"))



async def get_unique_field(collecion, column):
    return await collecion.distinct(column)


import asyncio
import motor.motor_asyncio

async def database_live_connect():
    gg_client = AsyncIOMotorClient(
    f"mongodb+srv://fiverr_user:fiverr_user@cluster0.sngd13i.mongodb.net/?retryWrites=true&w=majority",
    maxPoolSize=50,
)
    mvp2 = gg_client["mvp2"]
    mvp2_collection = mvp2["supplier_lookup"]

    return mvp2_collection

async def get_collection_length(collection):
    count = await collection.count_documents({})
    return count

async def main():
    collection = await database_live_connect()
    unique_seller_names = await get_collection_length(collection)
    print(unique_seller_names)


# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())

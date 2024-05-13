import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

username = 'fiverr_user'
password = 'fiverr_user'

async def fetch_records():
    # Connect to your MongoDB database
    gg_client = AsyncIOMotorClient(
    f"mongodb+srv://{username}:{password}@cluster0.sngd13i.mongodb.net/?retryWrites=true&w=majority",
    maxPoolSize=50,
)
    mvp2 = gg_client["mvp2"]
    mvp2_collection = mvp2["supplier_lookup"]

    # Retrieve the first 10 records
    cursor = mvp2_collection.find().limit(10)

    # Iterate over the cursor asynchronously
    records_to_fetch = []
    async for record in cursor:
        records_to_fetch.append(record)

    # Print the fetched records
    print(records_to_fetch)

# Run the coroutine asynchronously
asyncio.run(fetch_records())





async def get_unique_asin_with_highest_profit(collection):
    skip = 0
    limit = 3

    pipeline = [
        {"$match": {"profit_uk": {"$gt": 1}}},  # Filter documents where profit_uk > 1
        {"$group": {
            "_id": "$asin",
            "highest_profit": {"$max": "$profit_uk"}
        }},
        
        {"$skip": skip},  # Skip documents based on the offset
        {"$limit": limit},  # Limit the number of documents returned
        {"$project":
            {"_id": 0, "ref_close": 0, "ref_down": 0, "ref_limit": 0,
            'upc': 0, "ref_up": 0, "supplier_discount": 0, "brand_discount": 0,
            "awaiting validation": 0, "FBA_fee": 0, "Reff_fees": 0, "Categories_Root": 0, "delivery": 0,
            "Pack": 0}}
    ]

    unique_asin_with_highest_profit = await collection.aggregate(pipeline).to_list(None)
    print(unique_asin_with_highest_profit)
    return unique_asin_with_highest_profit




# async def get_total_unique_asins():
#     collection = mvp2["filter_supplier_lookup"]
#     pipeline = [
#         {"$group": {"_id": "$asin"}},  # Group by 'asin'
#         {"$count": "totalUniqueAsins"}  # Count the number of unique 'asin'
#     ]
#     result = await collection.aggregate(pipeline).to_list(None)
#     total_unique_asins = result[0]['totalUniqueAsins'] if result else 0
#     print(total_unique_asins)
#     return total_unique_asins



async def check_indexes():
    collection = mvp2["filter_supplier_lookup"]
    indexes = await collection.list_indexes().to_list(length=None)
    for index in indexes:
        print(index)

# Call the function to check indexes


async def drop_indexes():
    try:
        # Drop unnecessary indexes
        collection = mvp2["filter_supplier_lookup"]

        # await collection.drop_index("amz_Title")
        # await collection.drop_index("seller_name")
        # await collection.drop_index("search_term")
        await collection.drop_index("brand")
        # Repeat for other unnecessary indexes

        print("Indexes dropped successfully.")
    except Exception as e:
        print("Error dropping indexes:", e)

# Call the function to drop indexes


async def drop_index():
    try:
        # Drop the index
        collection = mvp2["filter_supplier_lookup"]
        await collection.drop_index("title_-1")
        print("Index dropped successfully.")
    except Exception as e:
        print("Error dropping index:", e)
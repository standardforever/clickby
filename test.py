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

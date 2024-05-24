from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from pymongo import DESCENDING

username = 'fiverr_user'
password = 'fiverr_user'
gg_client = AsyncIOMotorClient(
    f"mongodb+srv://{username}:{password}@cluster0.sngd13i.mongodb.net/?retryWrites=true&w=majority",
    maxPoolSize=50,
)

mvp2 = gg_client["mvp2"]



mvp2_collection_lookup = mvp2["profit_supplier_lookup"]
unique_collection_lookup = mvp2['unique_supplier_lookup']
mvp2_collection = mvp2["cn_supplier_lookup"]


async def get_unique_field(collection, column):
    distinct_values = await collection.distinct(column)
    print(len(distinct_values))
    return distinct_values

asyncio.run(get_unique_field(unique_collection_lookup, 'asin'))
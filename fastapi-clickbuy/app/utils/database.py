from motor.motor_asyncio import AsyncIOMotorClient
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()


# Retrieve environment variables
username = quote_plus(os.getenv("MONGO_USER"))
password = quote_plus(os.getenv("MONGO_PASS"))

async def database_live_connect():
    gg_client = AsyncIOMotorClient(
    f"mongodb+srv://{username}:{password}@cluster0.sngd13i.mongodb.net/?retryWrites=true&w=majority",
    maxPoolSize=50,
)
    mvp2 = gg_client["mvp2"]
    mvp2_collection = mvp2["unique_supplier_lookup"]
    mvp2_collection_profit = mvp2["profit_supplier_lookup"]
    return mvp2_collection, mvp2_collection_profit


async def connection():
    collection = await database_live_connect()
    document = await collection[0].find_one({})
    print(document)
    return collection
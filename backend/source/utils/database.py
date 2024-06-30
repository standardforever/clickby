from motor.motor_asyncio import AsyncIOMotorClient
from app.config import app_config

async def database_live_connect():
    gg_client = AsyncIOMotorClient(
    app_config.db_connection_url,
    maxPoolSize=50,
)
    mvp2 = gg_client[app_config.database_name]

    mvp2_collection = mvp2[app_config.unique_collection]
    mvp2_collection_profit = mvp2[app_config.profit_collection]
    return mvp2_collection, mvp2_collection_profit


async def connection():
    collection = await database_live_connect()
    document = await collection[0].find_one({})
    print(document)
    print(f"Print the total collection: {collection} ")
    return collection
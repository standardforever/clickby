from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

from helper_function.filter_collection import filter_collection
from helper_function.unique_collection import unique_asin

username = 'website_live'
password = '1mR6FOKNXrCcVtoP'
gg_client = AsyncIOMotorClient(
    f"mongodb+srv://{username}:{password}@cluster0.sngd13i.mongodb.net/?retryWrites=true&w=majority",
    maxPoolSize=50,
)

mvp2 = gg_client["mvp2"]



async def main():

    mvp2_collection_lookup = mvp2["profit_collection_production"]
    unique_collection_lookup = mvp2['unique_collection_production']
    mvp2_collection = mvp2["sp_lookup2"]

    await filter_collection(mvp2_collection_lookup, mvp2_collection)
    await unique_asin(mvp2_collection_lookup, unique_collection_lookup)


if __name__ == "__main__":
    asyncio.run(main())
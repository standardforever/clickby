from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from pymongo import DESCENDING
from helper_function.filter_collection import fetch_and_save_records
from helper_function.unique_collection import unique_asin

username = 'fiverr_user'
password = 'fiverr_user'
gg_client = AsyncIOMotorClient(
    f"mongodb+srv://{username}:{password}@cluster0.sngd13i.mongodb.net/?retryWrites=true&w=majority",
    maxPoolSize=50,
)

mvp2 = gg_client["mvp2"]



async def main():
    mvp2_collection_lookup = mvp2["profit_supplier_lookup"]
    unique_collection_lookup = mvp2['unique_supplier_lookup']
    mvp2_collection = mvp2["cn_supplier_lookup"]


    page = 1
    limit = 10000 # Set your desired batch size
    # await unique_collection_lookup.drop()

    if 'profit_supplier_lookup' not in await mvp2.list_collection_names():
        await mvp2_collection_lookup.create_index({'supplier_code': DESCENDING })
        await mvp2_collection_lookup.create_index({'profit_uk': DESCENDING })
        await mvp2_collection_lookup.create_index({'asin': DESCENDING })
        print("New index created succesfully")

    total_documents = await mvp2_collection.count_documents({"profit_uk": {"$gt": 1}})
    total_pages = -(-total_documents // limit)  # Ceiling division to calculate total pages
    print(f"Total documents: {total_documents}\n Total_pages: {total_pages}")

    # while page <= total_pages:
    #     try:
    #         await fetch_and_save_records(page, limit, mvp2_collection, mvp2_collection_lookup)
    #         page+=1
    #         print(f'PAGE: {page}')
    #     except Exception as e:
    #         print(f"Error processing batch: {e}")


    await unique_asin(mvp2_collection_lookup, unique_collection_lookup)




if __name__ == "__main__":
    asyncio.run(main())
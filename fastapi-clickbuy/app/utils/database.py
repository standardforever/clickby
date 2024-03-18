from motor.motor_asyncio import AsyncIOMotorClient
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()


local_client = AsyncIOMotorClient('mongodb://admin:supersecret@mongodb:27017')
filter = local_client['local_database']['filter_data']

# Retrieve environment variables
username = quote_plus(os.getenv("MONGO_USER"))
password = quote_plus(os.getenv("MONGO_PASS"))

amz_client = AsyncIOMotorClient(
    f"mongodb+srv://{username}:{password}@cluster0.sngd13i.mongodb.net/?retryWrites=true&w=majority",
    maxPoolSize=50,
)
amazon_db = amz_client["Vps_shopping_data"]

gg_client = AsyncIOMotorClient(
    f"mongodb+srv://{username}:{password}@cluster0.sngd13i.mongodb.net/?retryWrites=true&w=majority",
    maxPoolSize=50,
)
google_db = gg_client["Vps_shopping_data"]

async def get_collections():
    amazon_collection = amazon_db["amazon_combined2"]
    google_collection = google_db["unique_sc_data"]
    roi_collection = google_db["ROI"]

    # Initialize the new collection here
    item_count_collection = amazon_db["Item_Counts"]

    filtered_google_collection = amazon_db["filtered_google_data"]
    return amazon_collection, google_collection, item_count_collection, roi_collection,filtered_google_collection

async def filtered_google_data():
    filtered_google_collection = local_client['local_database']
    return filtered_google_collection




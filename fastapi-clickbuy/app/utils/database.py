from motor.motor_asyncio import AsyncIOMotorClient
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()


# Retrieve environment variables
username = quote_plus(os.getenv("MONGO_USER"))
password = quote_plus(os.getenv("MONGO_PASS"))


def database_live_connect():
    amz_client = AsyncIOMotorClient(
    f"mongodb+srv://{username}:{password}@cluster0.sngd13i.mongodb.net/?retryWrites=true&w=majority",
    maxPoolSize=50,
    )

    mvp2 = amz_client["mvp2"]
    mvp2_collection = mvp2["supplier_lookup"]
    return mvp2_collection


def database_local_connect():
    local_client = AsyncIOMotorClient('mongodb://admin:supersecret@mongodb:27017')
    local_collection = local_client['local_db']
    local_collection = local_collection['supplier_lookup']
    return local_collection
    

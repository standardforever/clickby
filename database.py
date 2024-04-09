from pymongo import MongoClient




username = 'fiverr_user'
password = 'fiverr_user'

# Connect to local MongoDB
local_client = MongoClient('mongodb://admin:supersecret@localhost:27017')
local_db = local_client['local_database']

# Connect to Google MongoDB
# gg_client = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.sngd13i.mongodb.net/")
# google_db = gg_client["Vps_shopping_data"]
# filter_collection = google_db["sc_data"]

# # Define the new collection in the local database
# filter_data_collection = local_db["sc_data"]


amazon_collection = local_db["tbl_amazon_product_masters3"]



amz_client = MongoClient(
    f"mongodb+srv://{username}:{password}@cluster0.sngd13i.mongodb.net/?retryWrites=true&w=majority",
    maxPoolSize=50,
)
amazon_db = amz_client["db_amazon_master"]

amazon_collection_client = amazon_db["tbl_amazon_product_masters3"]


def copy_data():
    # Fetch data with a limit from the filter collection in Google MongoDB
    cursor = amazon_collection_client.find({}).limit(1000)  # Limit to 10,000 documents

    # Extract documents from cursor
    documents = list(cursor)

    if documents:
        # Insert data into the filter_data collection in the local MongoDB using insert_many()
        result = amazon_collection.insert_many(documents)
        print(f"Inserted {len(result.inserted_ids)} documents")
    else:
        print("No documents found to copy")

# Call the function to copy data
copy_data()

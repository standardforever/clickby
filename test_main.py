from pymongo import MongoClient

# Local MongoDB connection
local_client = MongoClient(f'mongodb://admin:supersecret@localhost:27017')
local_db = local_client["local_db"]  # Change "local_db" to your desired local database name
local_collection = local_db["supplier_lookup"]  # Collection name in local database

# MongoDB Atlas connection
username = 'fiverr_user'
password = 'fiverr_user'
gg_client = MongoClient(
    f"mongodb+srv://{username}:{password}@cluster0.sngd13i.mongodb.net/?retryWrites=true&w=majority",
    maxPoolSize=50,
)
mvp2 = gg_client["mvp2"]
mvp2_collection = mvp2["supplier_lookup"]

# Function to fetch and save records
def fetch_and_save_records():
    # Retrieve the first 100 records
    skip = 0
    limit = 2000
    for i in range(20):
        cursor = mvp2_collection.find().skip(skip).limit(limit)

        # Insert all records into the local database
        records_to_insert = list(cursor)
        if records_to_insert:
            local_collection.insert_many(records_to_insert)
            print("Records saved to local database successfully!")
        else:
            print("No records found to save.")
    skip += 2000

# Call the function to fetch and save records
fetch_and_save_records()

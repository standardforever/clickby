from pymongo import MongoClient


local_clinet = MongoClient(f'mongodb://admin:supersecret@localhost:27017')
username = 'fiverr_user'
password = 'fiverr_user'

amz_client = MongoClient(
    f"mongodb+srv://{username}:{password}@cluster0.sngd13i.mongodb.net/?retryWrites=true&w=majority",
    maxPoolSize=50,
)
amazon_db = amz_client["db_amazon_master"]

gg_client = MongoClient(
    f"mongodb+srv://{username}:{password}@cluster0.sngd13i.mongodb.net/?retryWrites=true&w=majority",
    maxPoolSize=50,
)
google_db = gg_client["Vps_shopping_data"]

# db_amazon_master.tbl_amazon_product_masters3


def get_collections():
    amazon_collection = amazon_db["tbl_amazon_product_masters3"]
    google_collection = google_db["unique_sc_data"]
    roi_collection = google_db["ROI"]

    item_count_collection = google_db["Item_Counts"]
    sc_data = google_db["sc_data"]

    return amazon_collection, google_collection, item_count_collection, roi_collection, sc_data


(amazon_collection, _, _, _, filter) = get_collections()



print(amazon_collection.find_one({"asin": 'B09XMPYJBQ'}))
print('\n\n')
print(filter.find_one({'ASIN': 'B09XMPYJBQ'}))



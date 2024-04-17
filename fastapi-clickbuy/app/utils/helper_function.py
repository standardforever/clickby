from urllib.parse import urlparse

async def get_all_categories(collection):
    return await collection.distinct("Categories: Root")

# async def get_unique_field(collection, column):
#     distinct_values = await collection.distinct(column)
#     return distinct_values


async def get_unique_field(collection, column):
    # Define the query to filter documents with profit_uk > 1
    query = {"profit_uk": {"$exists": True, "$gt": 1}}
    # Get distinct values of the specified column from filtered documents
    distinct_values = await collection.distinct(column, query=query)
    return distinct_values


def is_ebay_url(url):
    return "ebay" in urlparse(url).netloc.lower()



def is_filtered_seller(seller_name):
    return "ebay" in seller_name.lower() or "onbuy" in seller_name.lower()



def is_amazon_seller(seller_name):
    return "amazon" in seller_name.lower()

def remove_duplicate_sellers(scraped_data):
    unique_sellers = {}
    for data in scraped_data:
        seller_name = data.get("seller_name")
        if seller_name not in unique_sellers:
            unique_sellers[seller_name] = data

    unique_scraped_data = list(unique_sellers.values())
    return sorted(
        unique_scraped_data,
        key=lambda x: float(x["seller_price"].replace("£", ""))
        if "£" in x["seller_price"]
        else float(x["seller_price"]),
    )

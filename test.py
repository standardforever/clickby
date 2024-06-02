from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from typing import Optional, List
import asyncio

# MongoDB connection
username = 'fiverr_user'
password = 'fiverr_user'
gg_client = AsyncIOMotorClient(
    f"mongodb+srv://{username}:{password}@cluster0.sngd13i.mongodb.net/?retryWrites=true&w=majority",
    maxPoolSize=50,
)

mvp2 = gg_client["mvp2"]
mvp2_collection = mvp2["unique_supplier_lookup"]

# class Item:
#     def __init__(self, **kwargs):
#         self.supplier_code = kwargs.get("supplier_code")
#         self.asin = kwargs.get("asin")
#         self.category = kwargs.get("category")
#         self.comparison_link_url = kwargs.get("comparison_link_url")
#         self.last_update_time = kwargs.get("last_update_time")
#         self.seller_name = kwargs.get("seller_name")
#         self.seller_price = kwargs.get("seller_price")
#         self.title = kwargs.get("title")
#         self.amazon_price = kwargs.get("amazon_price")
#         self.offers = kwargs.get("offers")
#         self.sales_rank = kwargs.get("sales_rank")
#         self.REF_fee = kwargs.get("REF_fee")
#         self.total_fees_UK = kwargs.get("total_fees_UK")
#         self.seller_price_numeric = kwargs.get("seller_price_numeric")
#         self.new_seller_price = kwargs.get("new_seller_price")
#         self.profit_uk = kwargs.get("profit_uk")
#         self.roi_uk = kwargs.get("roi_uk")
#         self.roi_category = kwargs.get("roi_category")

#     def __repr__(self):
#         return f"<Item asin={self.asin} seller_price={self.seller_price} profit_uk={self.profit_uk}>"

async def fetch_items(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: Optional[int] = 100
) :
    query = {}
    if start_date and end_date:
        query = {
            "last_update_time": {
                "$gte": start_date.strftime("%Y-%m-%d %H:%M:%S"),
                "$lt": (end_date + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    elif start_date:
        query = {
            "last_update_time": {
                "$gte": start_date.strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    elif end_date:
        query = {
            "last_update_time": {
                "$lt": (end_date + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
            }
        }

    # Sort the results by `last_update_time` in descending order and limit the results
    cursor = mvp2_collection.find(query).sort("last_update_time", -1).limit(limit)
    items = await cursor.to_list(length=None)
    return items
    return [Item(**item) for item in items]

# Example usage of the function
async def main():
    start_date_str = "2024-05-26"
    end_date_str = "2024-05-27"
    
    # If the date strings need to be converted to datetime objects
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    items = await fetch_items(start_date=start_date,  limit=10)

    for item in items:
        print(item)

if __name__ == "__main__":
    asyncio.run(main())

from pydantic import BaseModel
from typing import List, Union

class Category(BaseModel):
    categories: List[str]

class FilterModel(BaseModel):
    roi: List[str] = []
    categories: List[str] = []
    supplier_name: List[str] = []
    market_place: List[str] = []
    store_price: List[str] = []
    search_term: str = None
    skip: int = 0
    limit: int = 40
    


class ResponseBase(BaseModel):
    supplier_code: Union[str, None] = None
    asin: Union[str, None] = None
    category: Union[str, None] = None
    comparison_link_url: Union[str, None] = None
    last_update_time: Union[str, None] = None
    seller_name: Union[str, None] = None
    seller_price: Union[str, None] = None
    title: Union[str, None] = None
    upc: Union[int, None] = None
    amz_Title: Union[str, None] = None
    brand: Union[str, None] = None
    amazon_price: Union[str, None] = None
    Total_fees_UK: Union[float, None] = None

class ResponseModel(BaseModel):
    data: List[ResponseBase]
    total_count: int
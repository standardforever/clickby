from pydantic import BaseModel
from typing import List

class Category(BaseModel):
    categories: List[str]

class Filter(BaseModel):
    roi: List[str] = []
    categories: List[str] = []
    supplier_name: List[str] = []
    market_place: List[str] = []
    store_price: List[str] = []
    search_term: str = None
    skip: int = 0
    limit: int = 40
    

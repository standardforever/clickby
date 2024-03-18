from pydantic import BaseModel
from typing import List

class Category(BaseModel):
    categories: List[str]
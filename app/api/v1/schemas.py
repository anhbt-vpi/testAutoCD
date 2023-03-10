from typing import List, Optional, Any
from pydantic import BaseModel

class ItemBase(BaseModel):
    data: List[Any] = []

class FacetModel(BaseModel):
    tableName: List[Any] = []
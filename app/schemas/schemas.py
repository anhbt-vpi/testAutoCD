from typing import List, Optional, Any
from pydantic import BaseModel




class Item(BaseModel):
    ID: int
    RECORD_ID: int
    TIME_ID: Any
    CRUDEOIL_ID: str
    PRICE_TYPE: str
    EXCHANGES: str
    CPRICE_CRUDEOIL_VALUE: float
    UNIT_ID: str
    COUNTRY_ID: str


class ItemBase(BaseModel):
    data: List[Item] = []
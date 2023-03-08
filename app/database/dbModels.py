from sqlalchemy import Boolean, Column, Integer, String, Any, Float
from sqlalchemy.orm import relationship

from app.database.database import Base

class TableModel(Base):
    __tablename__ = "fact_oilprice_input"
    ID = Column(Integer, primary_key=True, index=True)
    RECORD_ID = Column(Integer)
    TIME_ID = Column(String(255))
    CRUDEOIL_ID = Column(String(255))
    PRICE_TYPE = Column(String(255))
    EXCHANGES = Column(String(255))
    CPRICE_CRUDEOIL_VALUE = Column(Float)
    UNIT_ID = Column(String(255))
    COUNTRY_ID = Column(String(255))

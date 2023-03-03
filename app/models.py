from sqlalchemy import Table, MetaData
from .database import engine

metadata = MetaData()
TableModel = Table('fact_oilprice_input', metadata, autoload_with=engine)

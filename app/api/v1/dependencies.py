from fastapi import HTTPException
from fastapi import Depends, Request
from app.database.database import connect_DB
from sqlalchemy import Table, MetaData
from app import config
from app.database.dbModels import getModel
from sqlalchemy import text


async def validate(request: Request):
    path_param = request.path_params.get("product")
    if path_param is None:
        raise HTTPException(status_code=400, detail=config.error_message.get("missing_product"))
    if path_param not in config.map_db.keys():
        raise HTTPException(status_code=400, detail=config.error_message.get("product_not_found"))


async def get_db(request: Request, map_db=config.map_db, validate=Depends(validate)):
    product = map_db.get(request.path_params.get("product"))
    server = product.get("server")
    database = product.get("database")
    SessionLocal = connect_DB(server, database)
    map_db = SessionLocal()
    try:
        yield map_db
    finally:
        map_db.close()




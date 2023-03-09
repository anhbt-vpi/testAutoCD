from fastapi import HTTPException
from fastapi import Depends, Request
from app.database.database import connect_DB
from sqlalchemy import Table, MetaData
from app import constant


async def lookup_table():
    server = constant.lookup_table.get("server")
    database = constant.lookup_table.get("database")
    SessionLocal = connect_DB(server, database)
    db = SessionLocal()
    metadata = MetaData()
    productInfo = Table(constant.lookup_table.get("tableName"), metadata,
                        autoload_with=db.bind)
    res = db.query(productInfo).all()
    lookup_table = {}
    for item in res:
        key = item[0]
        server = item[1]
        database = item[2]
        table_list = item[3].split(', ')
        lookup_table[key] = {
            "server": server,
            "database": database,
            "tableList": table_list
        }
    db.close()
    return lookup_table


async def get_db(request: Request, lookup_table=Depends(lookup_table)):
    server = lookup_table[request.path_params.get("product")]['server']
    database = lookup_table[request.path_params.get("product")]['database']
    SessionLocal = connect_DB(server, database)
    map_db = SessionLocal()
    try:
        yield map_db
    finally:
        map_db.close()


async def validate(request: Request, lookup_table=Depends(lookup_table)):
    path_param = request.path_params.get("product")
    if path_param is None:
        raise HTTPException(status_code=400, detail=constant.error_message.get("missing_product"))
    if path_param not in lookup_table.keys():
        raise HTTPException(status_code=400, detail=constant.error_message.get("product_not_found"))
    query_param = request.query_params._dict.get("tableName")
    if query_param is not None and query_param not in lookup_table[request.path_params.get("product")]['tableList']:
        raise HTTPException(status_code=400, detail=constant.error_message.get("table_not_found"))

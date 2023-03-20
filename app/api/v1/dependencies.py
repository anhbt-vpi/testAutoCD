from fastapi import HTTPException
from fastapi import Depends, Request
from app.database.database import connect_DB
from sqlalchemy import Table, MetaData
from app import config
from app.database.dbModels import getModel
from sqlalchemy import text
async def get_db(request: Request, map_db = config.map_db):
    product = map_db.get(request.path_params.get("product"))
    server = product.get("server")
    database = product.get("database")
    SessionLocal = connect_DB(server, database)
    map_db = SessionLocal()
    try:
        yield map_db
    finally:
        map_db.close()

async def get_tables(request: Request, db=Depends(get_db)):
    str_sql = text("SELECT table_name FROM information_schema.tables")
    result_query = db.execute(str_sql)
    results = result_query.fetchall()
    table_names = [row[0] for row in results]
    drop = ["relationshipColumns", "relationships", "database_firewall_rules"]
    list_table = [elem for elem in table_names if elem not in drop]
    return list_table

async def validate(request: Request, tables=Depends(get_tables)):
    path_param = request.path_params.get("product")
    tableName = request.path_params.get("tableName")
    if path_param is None:
        raise HTTPException(status_code=400, detail=config.error_message.get("missing_product"))
    if path_param not in config.map_db.keys():
        raise HTTPException(status_code=400, detail=config.error_message.get("product_not_found"))
    if tableName is not None and tableName not in tables:
        raise HTTPException(status_code=400, detail=config.error_message.get("table_not_found"))


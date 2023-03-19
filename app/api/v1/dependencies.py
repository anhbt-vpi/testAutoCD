from fastapi import HTTPException
from fastapi import Depends, Request
from app.database.database import connect_DB
from sqlalchemy import Table, MetaData
from app import config
from app.database.dbModels import getModel

async def lookup_table():
    server = config.lookup_table.get("server")
    database = config.lookup_table.get("database")
    SessionLocal = connect_DB(server, database)
    db = SessionLocal()
    productInfoModel = getModel(config.lookup_table.get("tableName"), db)
    res = db.query(productInfoModel).all()
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

map_db = {
    "crudeOil": {
        "server": "xznozrobo3funm76yoyaoh75wm-lvvgvquleiuurnfvyvnetw7hoq.datamart.pbidedicated.windows.net",
        "database": "Oil price forecast"
    },
    "lpg": {
        "server": "xznozrobo3funm76yoyaoh75wm-fr3e3p3dk6eejffi7w4p27iybe.datamart.pbidedicated.windows.net",
        "database": "2023_LPG_Datamart_Hanhdh"
    },
    "hydrogen": {
        "server": "xznozrobo3funm76yoyaoh75wm-bskk54c73wdejgsv4xf2kugg5i.datamart.pbidedicated.windows.net",
        "database": "Global_Hydrogen_Data"
    },
    "crudeOilV2": {
        "server": "xznozrobo3funm76yoyaoh75wm-joiz6h43v2cuxennbhz3uklaa4.datamart.pbidedicated.windows.net",
        "database": "Crude Oil Price V2"
    }
}
async def get_db(request: Request, map_db = map_db):
    product = map_db.get(request.path_params.get("product"))
    server = product.get("server")
    database = product.get("database")
    SessionLocal = connect_DB(server, database)
    map_db = SessionLocal()
    try:
        yield map_db
    finally:
        map_db.close()


async def validate(request: Request, lookup_table=Depends(lookup_table)):
    path_param = request.path_params.get("product")
    if path_param is None:
        raise HTTPException(status_code=400, detail=config.error_message.get("missing_product"))
    if path_param not in lookup_table.keys():
        raise HTTPException(status_code=400, detail=config.error_message.get("product_not_found"))
    query_param = request.query_params._dict.get("tableName")
    if query_param is not None and query_param not in lookup_table[request.path_params.get("product")]['tableList']:
        raise HTTPException(status_code=400, detail=config.error_message.get("table_not_found"))



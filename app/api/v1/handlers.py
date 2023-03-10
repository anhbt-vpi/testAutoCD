from fastapi import Request
from sqlalchemy.orm import Session
from app.database.dbModels import getModel


async def get_data(request: Request, lookup_table, db: Session):
    res = []
    tableList = lookup_table[request.path_params.get("product")]['tableList']

    if (request.query_params._dict.get("tableName")):

        TableModel = getModel(request.query_params._dict.get("tableName"), db)
        results = db.query(TableModel).all()
        for result in results:
            res.append(result._mapping)
    else:
        for item in tableList:
            TableModel = getModel(item, db)
            results = db.query(TableModel).all()
            obj = {
                "tableName": item,
                "data": []
            }
            for result in results:
                obj.get("data").append(result._mapping)
            res.append(obj)
    return {"data": res}


async def get_facet(request: Request, lookup_table):
    tableList = lookup_table[request.path_params.get("product")]['tableList']
    return {"tableName": tableList}

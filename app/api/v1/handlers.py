from fastapi import Request
from sqlalchemy.orm import Session
from app.database.dbModels import getModel


async def get_oil_price(request: Request, lookup_table, db: Session):
    res = []
    tableList = lookup_table[request.path_params.get("product")]['tableList']

    if(request.query_params._dict.get("tableName")):

        TableModel = getModel(request.query_params._dict.get("tableName"), db)
        results = db.query(TableModel).limit(10).all()
        for result in results:
            res.append(result._mapping)
    else:
        for item in tableList:
            TableModel = getModel(item, db)
            results = db.query(TableModel).limit(10).all()
            obj = {
                "tableName": item,
                "data": []
            }
            for result in results:
                obj.get("data").append(result._mapping)
            res.append(obj)
    return {"data": res}

from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from app.database.dbModels import getModel
from sqlalchemy import text
from sqlalchemy.types import Date, Integer, Float, BIGINT


async def get_data_filter(request: Request, db: Session):

    limit = request.query_params._dict.pop('limit', None)
    tableName = request.path_params.get("tableName")
    TableModel = getModel(tableName, db)
    condition = []

    for column in TableModel.columns:
        if isinstance(column.type, (Date, Integer, Float, BIGINT)):
            min = request.query_params._dict.pop(column.name + '_MIN', None)
            max = request.query_params._dict.pop(column.name + '_MAX', None)
            print(min, max)
            if max:
                condition.append(TableModel.c[column.name] <= max)
            if min:
                condition.append(TableModel.c[column.name] >= min)

    others = request.query_params._dict

    for key in others.keys():
        if key.rstrip('_MAX').rstrip('_MIN') not in TableModel.c.keys():
            raise HTTPException(status_code=422, detail=f"{key} not found in table {tableName}")

    for key, value in others.items():
        condition.append(TableModel.c[key] == value)

    results = db.query(TableModel)\
        .filter(*condition) \
        .limit(limit)\
        .all()
    res = []
    for result in results:
        res.append(result._mapping)

    return {"data": res}
async def get_all_data(request: Request, db: Session):

    tableName = request.path_params.get("tableName")
    TableModel = getModel(tableName, db)

    results = db.query(TableModel)\
        .all()
    res = []
    for result in results:
        res.append(result._mapping)

    return {"data": res}

async def get_tables(tables):
    return {"tables": tables}


async def get_columns(request: Request, db: Session):
    tableName = request.path_params.get("tableName")
    TableModel = getModel(tableName, db)
    new_result = [elem.name for elem in TableModel.columns]
    return {"columns": new_result}




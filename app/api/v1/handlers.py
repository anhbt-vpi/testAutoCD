from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from app.database.dbModels import getModel
from sqlalchemy import text
from sqlalchemy.types import Date, Integer, Float, BIGINT
from pydantic import BaseModel
from typing import List
class QueryResponse(BaseModel):
    data: List[dict]
    total_records: int
    records_returned: int

async def get_data_filter(request: Request, db: Session):

    responseContainer = {}
    request_info = {"endpoint": request.url.path,
                    "params": dict(request.query_params)}
    haveLength = request.query_params._dict.get("length")
    length = int(request.query_params._dict.pop('length', 5000))
    orderby = request.query_params._dict.pop('orderby', None)
    offset = int(request.query_params._dict.pop('offset', 0))
    tableName = request.path_params.get("tableName")
    TableModel = getModel(tableName, db)
    condition = []
    try:
        str_sql = text("SELECT table_name FROM information_schema.tables")
        result_query = db.execute(str_sql)
        results = result_query.fetchall()
        table_names = [row[0] for row in results]
        drop = ["relationshipColumns", "relationships", "database_firewall_rules"]
        list_table = [elem for elem in table_names if elem not in drop]
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something wrong, contact your admin")
    if tableName is not None and tableName not in list_table:
        raise HTTPException(status_code=400, detail="Table not found. Please check your table name again")

    if orderby is not None and orderby not in TableModel.c.keys():
        raise HTTPException(status_code=400, detail=f"order by column {orderby} not found in table {tableName}")
    if offset != 0 and orderby is None:
        error = {
            "errorMsg": "order by is required when you want to use offset",
            "code": 400
        }
        raise HTTPException(status_code=400, detail=error)
    for column in TableModel.columns:
        if isinstance(column.type, (Integer, Float, BIGINT)):
            min = request.query_params._dict.pop('Min_' + column.name, None)
            max = request.query_params._dict.pop('Max_' + column.name, None)
            if max:
                condition.append(TableModel.c[column.name] <= max)
            if min:
                condition.append(TableModel.c[column.name] >= min)
        if isinstance(column.type, (Date)):
            min = request.query_params._dict.pop('Start_' + column.name, None)
            max = request.query_params._dict.pop('End_' + column.name, None)
            if max:
                condition.append(TableModel.c[column.name] <= max)
            if min:
                condition.append(TableModel.c[column.name] > min)

    others = request.query_params._dict

    for key in others.keys():
        if key.rstrip('_MAX').rstrip('_MIN') not in TableModel.c.keys():
            error = {
                "errorMsg": f"{key} not found in table {tableName}",
                "code": 400
            }
            raise HTTPException(status_code=400, detail=error)

    for key, value in others.items():
        condition.append(TableModel.c[key] == value)
    total_records = db.query(TableModel).count()
    try:
        if offset and orderby:
            results = db.query(TableModel) \
                .filter(*condition) \
                .order_by(TableModel.c[orderby]) \
                .offset(offset) \
                .limit(length) \
                .all()
        else:
            results = db.query(TableModel) \
                .filter(*condition) \
                .limit(length) \
                .all()
        res = []
        for result in results:
            res.append(result._mapping)
    except Exception as e:
        error = {
            "errorMsg": "Something wrong, contact your admin",
            "code": 400
        }
        raise HTTPException(status_code=400, detail=error)
    if len(res) == 0:
        error = {
            "errorMsg": "No records found with your input",
            "code": 404
        }
        raise HTTPException(status_code=404, detail=error)
    if total_records > 5000 and length >= 5000 and not haveLength:
        responseContainer["warnings"] = {
            "warning": "incomplete return",
            "description": "The API can only return 5000 rows in JSON format.  Please consider constraining your request with parameters or using offset to paginate results."
        }
    responseContainer["response"] = {"total_records": total_records, "records_returned": len(res), "offset": offset, "orderby": orderby, "data": res}
    responseContainer["request"] = request_info
    responseContainer["apiVersion"] = "0.0.1"

    return responseContainer


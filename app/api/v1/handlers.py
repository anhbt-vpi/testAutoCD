from fastapi import Request
from sqlalchemy.orm import Session
from app.database.dbModels import getModel
from sqlalchemy import text


async def get_data(request: Request, db: Session):
    res = []
    TableModel = getModel(request.path_params.get("tableName"), db)
    # TableModel = getModel(request.query_params._dict.get("tableName"), db)
    results = db.query(TableModel).all()
    for result in results:
        res.append(result._mapping)

    return {"data": res}


async def get_table_name(request: Request, db: Session):
    str_sql = text("SELECT table_name FROM information_schema.tables")
    result_query = db.execute(str_sql)
    results = result_query.fetchall()
    table_names = [row[0] for row in results]
    drop = ["relationshipColumns", "relationships", "database_firewall_rules"]
    new_result = [elem for elem in table_names if elem not in drop]
    return {"tableName": new_result}




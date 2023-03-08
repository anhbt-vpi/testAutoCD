from fastapi import Request
from sqlalchemy.orm import Session
from app.database import dbModels


async def get_oil_price(db: Session, request: Request):
    start_date = request.query_params._dict.pop('start_date', None)
    end_date = request.query_params._dict.pop('end_date', None)
    limit = request.query_params._dict.pop('limit', None)
    others = request.query_params._dict
    # for key in others.keys():
    #     if key not in TableModel.c.keys():
    #         raise HTTPException(status_code=422, detail= f"{key} not found in model columns")
    condition = []
    if end_date:
        condition.append(dbModels.TableModel.TIME_ID <= end_date)
    if start_date:
        condition.append(dbModels.TableModel.TIME_ID >= start_date)
    #
    # for key, value in others.items():
    #     condition.append(TableModel.c[key] == value)
    results = db.query(dbModels.TableModel) \
        .filter(*condition) \
        .limit(limit) \
        .all()

    return {"data": results}

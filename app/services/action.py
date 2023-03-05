from sqlalchemy.orm import Session

# from ..models.models import TableModel
from app.schemas.schemas import *
from fastapi import HTTPException
from app import models

def get_oil_prices(db: Session, param : Any={}):

    start_date = param.pop('start_date', None)
    end_date = param.pop('end_date', None)
    limit = param.pop('limit', None)
    others = param

    # for key in others.keys():
    #     if key not in TableModel.c.keys():
    #         raise HTTPException(status_code=422, detail= f"{key} not found in model columns")
    #
    # condition = []
    # if end_date:
    #     condition.append(TableModel.c["TIME_ID"] <= end_date)
    # if start_date:
    #     condition.append(TableModel.c["TIME_ID"] >= start_date)
    #
    # for key, value in others.items():
    #     condition.append(TableModel.c[key] == value)

    # results = db.query(TableModel)\
    #     .filter(*condition) \
    #     .limit(limit)\
    #     .all()
    res = []
    # for result in results:
    #     res.append(result._mapping)
    return res


from fastapi import Request
from sqlalchemy.orm import Session
from app.database import dbModels


async def get_oil_price(db: Session, request: Request):
    results = db.query(dbModels.TableModel).limit(10).all()
    res = []
    for result in results:
        res.append(result._mapping)
    return {"data": res}

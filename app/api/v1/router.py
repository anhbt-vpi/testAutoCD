from fastapi import APIRouter
from app.database.database import SessionLocal
from app.api.v1 import resModels, handlers
from fastapi import Depends, Request
from sqlalchemy.orm import Session

router = APIRouter()


def get_db():
    map_db = SessionLocal()
    try:
        yield map_db
    finally:
        map_db.close()

@router.get("/products/crudeOil/international/price/daily", response_model=resModels.ItemBase)
async def get_price(request: Request, db: Session = Depends(get_db)):
    return await handlers.get_oil_price(db, request=request)

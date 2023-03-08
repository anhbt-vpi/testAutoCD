from fastapi import APIRouter
from app.database.database import SessionLocal
from app.api.handlers import get_oil_price
from fastapi import Depends, Request
from sqlalchemy.orm import Session

router = APIRouter()


def get_db():
    map_db = SessionLocal()
    try:
        yield map_db
    finally:
        map_db.close()


# , response_model=oil_schemas.ItemBase
@router.get("/products/crudeOil/international/price/daily")
async def get_price(request: Request, db: Session = Depends(get_db)):
    return await get_oil_price(db, request=request)

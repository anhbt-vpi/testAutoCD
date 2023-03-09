from fastapi import APIRouter
from app.api.v1 import schemas, handlers, dependencies
from fastapi import Depends, Request
from app import constant

router = APIRouter()

@router.get(constant.endpoints.get("datamart"), response_model=schemas.ItemBase)
async def get_data(request: Request, validate=Depends(dependencies.validate),
                   lookup_table=Depends(dependencies.lookup_table),
                   db=Depends(dependencies.get_db)):
    return await handlers.get_oil_price(request=request, lookup_table=lookup_table, db=db)

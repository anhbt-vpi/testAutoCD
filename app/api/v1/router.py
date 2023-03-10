from fastapi import APIRouter
from app.api.v1 import schemas, handlers, dependencies
from fastapi import Depends, Request
from app import config

router = APIRouter()

@router.get("/products/{product}/facet", response_model=schemas.FacetModel)
async def get_facet(request: Request, validate=Depends(dependencies.validate),
                   lookup_table=Depends(dependencies.lookup_table)):
    return await handlers.get_facet(request=request, lookup_table=lookup_table)
@router.get("/products/{product}", response_model=schemas.ItemBase)
async def get_data(request: Request, validate=Depends(dependencies.validate),
                   lookup_table=Depends(dependencies.lookup_table),
                   db=Depends(dependencies.get_db)):
    return await handlers.get_data(request=request, lookup_table=lookup_table, db=db)

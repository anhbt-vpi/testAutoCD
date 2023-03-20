from fastapi import APIRouter
from app.api.v1 import schemas, handlers, dependencies
from fastapi import Depends, Request
from app import config

router = APIRouter()

@router.get("/products/{product}/tables/{tableName}/columns")
async def get_columns(request: Request, validate=Depends(dependencies.validate),
                   db=Depends(dependencies.get_db)):
    if request.query_params._dict:
        return await handlers.get_data_filter(request=request, db=db)
    else:
        return await handlers.get_columns(request=request, db=db)

@router.get("/products/{product}/tables/{tableName}")
async def get_data(request: Request, validate=Depends(dependencies.validate),
                   db=Depends(dependencies.get_db)):
    return await handlers.get_all_data(request=request, db=db)
@router.get("/products/{product}/tables")
@router.get("/products/{product}")
async def get_data(request: Request, validate=Depends(dependencies.validate),
                   db=Depends(dependencies.get_db), tables=Depends(dependencies.get_tables)):
    return await handlers.get_tables(tables=tables)

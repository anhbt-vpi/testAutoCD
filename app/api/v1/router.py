from fastapi import APIRouter
from app.api.v1 import schemas, handlers, dependencies
from fastapi import Depends, Request
from app import config

router = APIRouter()

@router.get("/{product}/{tableName}")
async def get_columns(request: Request, validate=Depends(dependencies.validate),
                   db=Depends(dependencies.get_db)):
    return await handlers.get_data_filter(request=request, db=db)



from fastapi import APIRouter
from app.api.v1 import schemas, handlers, dependencies
from fastapi import Depends, Request
from app import config

router = APIRouter()

# @router.get("/products/{product}/tables")
# async def read_user(request: Request, validate=Depends(dependencies.validate),
#                    lookup_table=Depends(dependencies.lookup_table),
#                    db=Depends(dependencies.get_db)):
#     return await handlers.get_data(request=request, lookup_table=lookup_table, db=db)
@router.get("/products/{product}/tables/{tableName}")
@router.get("/products/{product}/tables")
async def get_data(request: Request,
                   db=Depends(dependencies.get_db)):
    path_params = request.path_params
    if "tableName" in path_params:
        # return post info for the given user and post IDs
        tableName = path_params["tableName"]
        print("helo", tableName)
        return await handlers.get_data(request=request, db=db)
    else:
        # return user info for the given user ID
        print("no table Name")
        return await handlers.get_table_name(request=request, db=db)

# @router.get("/products/{product}", response_model=schemas.FacetModel)
# async def get_data(request: Request, validate=Depends(dependencies.validate),
#                    lookup_table=Depends(dependencies.res)):
#     return await handlers.get_table_name(request=request, lookup_table=lookup_table)
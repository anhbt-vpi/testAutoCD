from fastapi import Depends, FastAPI, Request
from .models import models
from .services import action
from app.database.database import SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

# Dependency
def get_db():
    map_db = SessionLocal()
    try:
        yield map_db
    finally:
        map_db.close()

# , response_model=schemas.ItemBase
@app.get("/products/{product}/international/price/daily")
async def get_price(request: Request, map_db: Session = Depends(get_db)):

    print("again")
    query_param = request.query_params._dict
    db_map_name = request.path_params["product"]

    # session = create_session(server_name, db_map_name)

    if len(query_param)==0:
        results = {"facet": {},
                   "params": models.TableModel.c.keys()}
    else:
        results = action.get_oil_prices(map_db, query_param)


    return { "data": results}

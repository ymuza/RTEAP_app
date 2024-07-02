import sys

from ..responses import successful_response

sys.path.append("..")  # allows to import everything in rteap parent directory

from fastapi import APIRouter, Depends, UploadFile, File

from sqlalchemy.orm import Session
from ..schemas import Product
from ..database import Base, SessionLocal, engine
from ..models import Products
from ..exceptions import get_user_exception
from ..routers.auth import get_current_user
router = APIRouter(
    prefix="/products", tags=["products"], responses={404: {"description": "not found"}}
)

Base.metadata.create_all(bind=engine)  # creates the database (tables & columns)


def get_db():
    """conects to the db"""
    data_base = None
    try:
        data_base = SessionLocal()  # starts the data_base session
        yield data_base
    finally:
        data_base.close()  # close the data_base session regardless of the use


@router.get("/")
async def read_all(
        data_base: Session = Depends(get_db),
):  # as session depends on get_data_base, we are sure to close the connection
    """gets all the records"""
    return data_base.query(Products).all()  # returns all the records


@router.post("/")
async def add_product(product: Product, image: UploadFile = File(...),
                      user: dict = Depends(get_current_user), data_base: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    product_model = Products()
    product_model.price = product.price
    product_model.description = product.description
    product_model.image = product.U
    product_model.complete = product.complete
    product_model.owner_id = user.get("id")

    data_base.add(product_model)  # places an object in the session
    data_base.commit()  # flushes changes and COMMITS () the change

    return successful_response(200)





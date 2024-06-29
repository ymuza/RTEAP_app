import sys

sys.path.append("..")  # allows to import everything in todos parent directory
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database import Base, SessionLocal, engine
from ..models import Products

router = APIRouter(
    prefix="/todos", tags=["todos"], responses={404: {"description": "not found"}}
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
    return data_base.query(Products).all()  # returns all the records from the Todos
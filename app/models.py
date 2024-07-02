from sqlalchemy import (Boolean, Column, Float, ForeignKey, Integer,
                        LargeBinary, String)
from sqlalchemy.orm import relationship

from app.database import Base


class Users(Base):
    """Users table"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    phone_number = Column(String)
    address_id = Column(Integer, ForeignKey("address.id"), nullable=True)
    todos = relationship(
        "Products", back_populates="owner"
    )  # creates the relationship with table "Products"
    address = relationship("Address", back_populates="user_address")


class Products(Base):
    """products table"""

    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    image = Column(LargeBinary)
    owner_id = Column(Integer, ForeignKey("users.id"))  # fk in table Users

    owner = relationship("Users", back_populates="products")


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, index=True)
    address1 = Column(String)
    address2 = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    postalcode = Column(String)
    apartment_number = Column(Integer)

    user_address = relationship("Users", back_populates="address")

from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float


class CreateUser(BaseModel):
    """User table data"""

    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
    phone_number: Optional[str]


class CreateAdminUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    phone_number: int
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str

from typing import Optional

from pydantic import BaseModel


class Products(BaseModel):
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

import sys
from datetime import datetime, timedelta, timezone
from typing import Optional
import secrets
from ..database import SessionLocal, engine
from ..password_management import get_password_hash, verify_password
from ..exceptions import get_user_exception, token_exception
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..models import Base, Users, AdminUsers
from ..schemas import CreateUser, CreateAdminUserRequest, Token
from starlette import status

sys.path.append("..")  # this will allow to import everything in auth's parent directory

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"

# creates the db and does all the important stuff for the table
Base.metadata.create_all(bind=engine)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def authenticate_user(username: str, password: str, db):
    """authenticates user"""
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


router = APIRouter(
    prefix="/Auth", tags=["auth"], responses={401: {"user": "Not authorized"}}
)


# instead of starting auth as an app,I extend the capability to main.
# prefix, tags and responses are a way of organizing the api.


def get_db():
    """retrieves the conection to the db"""
    data_base = None
    try:
        data_base = SessionLocal()
        yield data_base
    finally:
        data_base.close()


db_dependency = Annotated[Session, Depends(get_db)]


def create_access_token(
    username: str, user_id: int, expires_delta: Optional[timedelta] = None
):
    """creates the access token for the user"""
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expires = datetime.now(timezone.utc) + expires_delta
    else:
        expires = datetime.now(timezone.utc) + timedelta(minutes=15)

    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """gets current user"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return {"username": username, "id": user_id}
    except JWTError as exc:
        raise get_user_exception() from exc


@router.post(
    "/create/user"
)  # change app for router to extend the capability to main file
async def create_new_user(
    create_user: CreateUser, data_base: Session = Depends(get_db)
):
    """creates a new user in the db"""
    create_user_model = Users()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.firstname = create_user.first_name
    create_user_model.lastname = create_user.last_name
    create_user_model.phone_number = create_user.phone_number

    hash_password = get_password_hash(
        create_user.password
    )  # proceed to hash user password
    create_user_model.hashed_password = hash_password

    data_base.add(create_user_model)
    data_base.commit()

    return {"user has been added."}


@router.post("/create_admin_user", status_code=status.HTTP_201_CREATED)
async def create_user(
    db: db_dependency, create_admin_user_request: CreateAdminUserRequest
):
    create_admin_user_model = AdminUsers(
        username=create_admin_user_request.username,
        email=create_admin_user_request.email,
        firstname=create_admin_user_request.first_name,
        lastname=create_admin_user_request.last_name,
        hashed_password=create_admin_user_request.hashed_password,
        phone_number=create_admin_user_request.phone_number,
        role=create_admin_user_request.role,
        is_active=True,
    )
    db.add(create_admin_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    """returns the access token for the user"""
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=20)

    token = create_access_token(user.username, user.id, expires_delta=token_expires)

    return {'access_token': token, 'token_type': 'bearer'}

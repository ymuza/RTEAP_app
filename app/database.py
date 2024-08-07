from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = "postgresql://yamil:123456@db:5432/rteap"  # to use with docker

SQLALCHEMY_DATABASE_URL = "postgresql://yamil:32874993@localhost:5432/rteap"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = (
    declarative_base()
)  # contains a metadata object where new tables objects are collected.

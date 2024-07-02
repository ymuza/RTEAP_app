from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://yamil:32874993@localhost:5432/rteap"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def drop_all_tables():
    Base.metadata.drop_all(bind=engine)

if __name__ == "__main__":
    drop_all_tables()

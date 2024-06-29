from fastapi import Depends, FastAPI
from app.routers import product_service

app = FastAPI()

#Base.metadata.create_all(bind=engine)  # creates the database (tables & columns)

app.include_router(product_service.router)


@app.get("healthy")
def health_check():
    return {'status': 'healthy'}



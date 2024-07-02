from fastapi import Depends, FastAPI
import sys
import os
from app.routers import product_service, users_service, auth

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()


app.include_router(auth.router)
app.include_router(product_service.router)
app.include_router(users_service.router)


@app.get("healthy")
def health_check():
    return {'status': 'healthy'}

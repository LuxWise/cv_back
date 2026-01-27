from fastapi import FastAPI
from app.api.api import api_router

app = FastAPI(title="CV Back API", version="1.0.0")

app.include_router(api_router, prefix="/api")
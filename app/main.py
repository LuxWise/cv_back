from fastapi import FastAPI
from app.api.api import api_router
from app.core.logging import LoggingMiddleware

app = FastAPI(title="CV Back API", version="1.0.0")
app.add_middleware(LoggingMiddleware)

app.include_router(api_router, prefix="/api")
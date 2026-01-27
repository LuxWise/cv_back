from fastapi import APIRouter, Depends
from app.core.auth import authGuard
from app.core.database import Base, engine
from app.api.endpoints import users, auth, cv, register, generate

Base.metadata.create_all(bind=engine)

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"], dependencies=[Depends(authGuard)])
api_router.include_router(register.router, prefix="/register", tags=["register"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(cv.router, prefix="/cv", tags=["cv"], dependencies=[Depends(authGuard)])
api_router.include_router(generate.router, prefix="/generate", tags=["generate"], dependencies=[Depends(authGuard)])
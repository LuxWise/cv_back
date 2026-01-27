from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import AuthLogin, AuthResponse
from app.services import auth_services

router = APIRouter()

@router.post("/login", response_model=AuthResponse)
async def login(auth: AuthLogin,  db: Session = Depends(get_db)):
    result = auth_services.login(db, auth)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return result
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserRegister
from app.services import user_service

router = APIRouter()

@router.post("")
async def create_user(user: UserRegister, db: Session = Depends(get_db)):
    return await user_service.register(db=db, user=user)

@router.post("/confirm")
async def confirm_user_registration(code: str, db: Session = Depends(get_db)):
    return await user_service.confirm_registration(db=db, code=code)
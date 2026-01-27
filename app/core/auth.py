import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.database import get_db
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.core.vault import *
from app.services import user_service
from typing import Optional

load_dotenv()

JWT_SECRET_KEY = get_jwt_secret_key()
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    
def authGuard(
    token: str = Depends(oauth2_scheme),
) : 
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: Optional[int] = payload.get("sub")

        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db: Session = next(get_db())
    user = user_service.get_user_service_by_id(db, user_id=user_id)
    if user is None:
        raise credentials_exception
    
    return user
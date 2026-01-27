from sqlalchemy.orm import Session
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.schemas.auth import AuthLogin

def login(db: Session, auth: AuthLogin):
    user = db.query(User).filter(User.email == auth.email).first()

    print("User fetched for login:", user)

    if not user:
        return None
    
    verified = verify_password(auth.password, user.password)
    if not verified:
        return None
    
    try:
        payload = { "sub": str(user.id), "email": user.email }
        token = create_access_token(payload)
        return {"access_token": token, "message": "Login successful"}
    except Exception as e:
        return None


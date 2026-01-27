from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.core.vault import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET_KEY = get_jwt_secret_key()

PRIVATE_KEY = get_JWT_private_key()
ISSUER = get_JWT_issuer()
AUDIENCE = get_JWT_audience()

def hash_password(password: str) -> str:
    return pwd_context.hash(password, rounds=10)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(payload: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = payload.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=60))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm='HS256')
    return encoded_jwt

def create_register_token(
        user_id: int, 
        email: str, 
        password: str, 
        first_name: str, 
        last_name: str
    ):
    payload = {
        "sub": user_id,
        "user_id": user_id,
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "iss": ISSUER,
        "aud": AUDIENCE,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=5)
    }
    token = jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')

    return token

from pydantic import BaseModel, ConfigDict, EmailStr

class AuthLogin(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    access_token: str
    message: str
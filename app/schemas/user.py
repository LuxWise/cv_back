from pydantic import BaseModel, ConfigDict, EmailStr

class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class UserRegister(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
from typing import Optional
from pydantic import EmailStr, BaseModel


class UserSingUp(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class UserAuth(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserDetail(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    password: str
    is_superuser: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
    is_superuser: Optional[bool] = None

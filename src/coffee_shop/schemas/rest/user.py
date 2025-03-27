from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserUpdateMe(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)


class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=8)


class UserInDBBase(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserInDB(UserInDBBase):
    hashed_password: str


class User(UserInDBBase):
    pass

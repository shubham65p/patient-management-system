from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field(default="staff")
    is_active: bool = Field(default=True)

    class Config:
        extra = 'forbid'


class UserLogin(BaseModel):
    username: str
    password: str


class UserInDB(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: Optional[datetime] = None

    class Config:
        extra = 'forbid'

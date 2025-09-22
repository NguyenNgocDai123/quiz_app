from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from app.constants.enums.roles import RoleEnum


class UserBase(BaseModel):
    full_name: str
    email: EmailStr


class UserCreate(UserBase):
    full_name: str
    email: EmailStr
    password: str
    role: Optional[RoleEnum] = RoleEnum.USER


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserOut(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

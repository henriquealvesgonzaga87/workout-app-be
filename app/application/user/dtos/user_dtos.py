from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class CreateUserDto(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_active: bool = True
    is_super_admin: bool = False
    creation_date: datetime
    update_date: Optional[datetime] = None


class UserOutputDto(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str
    is_active: bool

    class Config:
        from_attributes = True

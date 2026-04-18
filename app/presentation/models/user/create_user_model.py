from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_super_admin: Optional[bool] = False


class UpdateUserRequest(BaseModel):
    name: Optional[str | None] = None
    email: Optional[EmailStr | None] = None
    password: Optional[str | None] = None
    is_active: Optional[bool | None] = None
    is_super_admin: Optional[bool | None] = None


class CreateUserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str
    is_active: bool
    creation_date: datetime
    update_date: Optional[datetime] = None

    class Config:
        from_attributes = True

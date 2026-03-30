from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class CreateUserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str
    is_active: bool

    class Config:
        from_attributes = True

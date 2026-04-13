from pydantic import BaseModel, EmailStr


class JwtLoginDto(BaseModel):
    email: EmailStr
    password: str


class JwtTokenSchemaOutputDto(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

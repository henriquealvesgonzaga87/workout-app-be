from pydantic import BaseModel, EmailStr


class JwtLoginRequest(BaseModel):
    email: EmailStr
    password: str


class JwtTokenSchemaResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

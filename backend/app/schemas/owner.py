from pydantic import BaseModel, EmailStr


class OwnerRegister(BaseModel):
    owner_name: str
    email: EmailStr
    password: str


class OwnerLogin(BaseModel):
    email: EmailStr
    password: str


class OwnerResponse(BaseModel):
    id: int
    owner_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
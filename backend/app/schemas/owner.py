from pydantic import BaseModel, EmailStr, Field


class OwnerRegister(BaseModel):
    owner_name: str
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)


class OwnerLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)


class OwnerResponse(BaseModel):
    id: int
    owner_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
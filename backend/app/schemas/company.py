from pydantic import BaseModel, EmailStr
from typing import Optional


class CompanyCreate(BaseModel):
    company_name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    state: Optional[str] = None


class CompanyUpdate(BaseModel):
    company_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    state: Optional[str] = None


class CompanyResponse(BaseModel):
    id: int
    owner_id: int
    company_name: str
    address: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    state: Optional[str]

    class Config:
        from_attributes = True
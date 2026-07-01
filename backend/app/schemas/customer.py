from pydantic import BaseModel, EmailStr
from typing import Optional


class CustomerCreate(BaseModel):
    customer_name: str
    phone: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pin_code: Optional[str] = None
    gst_number: Optional[str] = None


class CustomerUpdate(BaseModel):
    customer_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pin_code: Optional[str] = None
    gst_number: Optional[str] = None


class CustomerResponse(BaseModel):
    id: int
    company_id: int
    customer_name: str
    phone: str
    email: Optional[EmailStr]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    pin_code: Optional[str]
    gst_number: Optional[str]

    class Config:
        from_attributes = True
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class ProductCreate(BaseModel):
    product_name: str
    unit: str
    price_per_unit: Decimal
    description: Optional[str] = None


class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    unit: Optional[str] = None
    price_per_unit: Optional[Decimal] = None
    description: Optional[str] = None


class ProductResponse(BaseModel):
    id: int
    company_id: int
    product_name: str
    unit: str
    price_per_unit: Decimal
    description: Optional[str]

    class Config:
        from_attributes = True
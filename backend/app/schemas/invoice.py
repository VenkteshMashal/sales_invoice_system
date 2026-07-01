from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import date


class InvoiceItemCreate(BaseModel):
    product_id: int
    quantity: Decimal


class InvoiceCreate(BaseModel):
    customer_id: int
    invoice_date: date
    gst_amount: Optional[Decimal] = Decimal("0.00")
    items: List[InvoiceItemCreate]


class InvoiceItemResponse(BaseModel):
    id: int
    product_id: int
    item_name: str
    quantity: Decimal
    unit: str
    price_per_unit: Decimal
    amount: Decimal

    class Config:
        from_attributes = True


class InvoiceResponse(BaseModel):
    id: int
    company_id: int
    customer_id: int
    invoice_number: str
    invoice_date: date
    sub_total: Decimal
    gst_amount: Decimal
    total_amount: Decimal
    paid_amount: Decimal
    balance_amount: Decimal
    amount_in_words: str
    payment_status: str
    items: List[InvoiceItemResponse]

    class Config:
        from_attributes = True
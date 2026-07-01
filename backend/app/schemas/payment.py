from pydantic import BaseModel
from decimal import Decimal


class PaymentUpdate(BaseModel):
    paid_amount: Decimal
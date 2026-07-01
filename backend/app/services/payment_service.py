from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.invoice import Invoice
from app.services.invoice_service import get_invoice_by_id


def update_invoice_payment(
    invoice_id: int,
    company_id: int,
    owner_id: int,
    payment_data,
    db: Session
):
    invoice = get_invoice_by_id(invoice_id, company_id, owner_id, db)

    paid_amount = Decimal(payment_data.paid_amount)

    if paid_amount < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Paid amount cannot be negative"
        )

    if paid_amount >= invoice.total_amount:
        invoice.paid_amount = invoice.total_amount
        invoice.balance_amount = Decimal("0.00")
        invoice.payment_status = "Paid"
    elif paid_amount == 0:
        invoice.paid_amount = Decimal("0.00")
        invoice.balance_amount = invoice.total_amount
        invoice.payment_status = "Unpaid"
    else:
        invoice.paid_amount = paid_amount
        invoice.balance_amount = invoice.total_amount - paid_amount
        invoice.payment_status = "Partial"

    db.commit()
    db.refresh(invoice)

    return invoice
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.security import get_current_owner
from app.models.owner import Owner
from app.schemas.payment import PaymentUpdate
from app.schemas.invoice import InvoiceResponse
from app.services.payment_service import update_invoice_payment

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.put("/invoice/{invoice_id}/company/{company_id}", response_model=InvoiceResponse)
def update_payment(
    invoice_id: int,
    company_id: int,
    payment_data: PaymentUpdate,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return update_invoice_payment(
        invoice_id,
        company_id,
        current_owner.id,
        payment_data,
        db
    )
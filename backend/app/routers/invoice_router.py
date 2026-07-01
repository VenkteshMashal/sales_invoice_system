from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.security import get_current_owner
from app.models.owner import Owner
from app.schemas.invoice import InvoiceCreate, InvoiceResponse
from app.services.invoice_service import (
    create_invoice,
    get_invoices,
    get_invoice_by_id
)

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)


@router.post("/company/{company_id}", response_model=InvoiceResponse)
def add_invoice(
    company_id: int,
    invoice_data: InvoiceCreate,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return create_invoice(company_id, current_owner.id, invoice_data, db)


@router.get("/company/{company_id}", response_model=list[InvoiceResponse])
def view_invoices(
    company_id: int,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return get_invoices(company_id, current_owner.id, db)


@router.get("/{invoice_id}/company/{company_id}", response_model=InvoiceResponse)
def view_invoice(
    invoice_id: int,
    company_id: int,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return get_invoice_by_id(invoice_id, company_id, current_owner.id, db)
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.security import get_current_owner
from app.models.owner import Owner
from app.models.invoice import Invoice
from app.models.company import Company
from app.models.customer import Customer
from app.services.invoice_service import get_invoice_by_id
from app.utils.pdf_generator import generate_invoice_pdf

router = APIRouter(
    prefix="/pdf",
    tags=["PDF"]
)


@router.get("/invoice/{invoice_id}/company/{company_id}")
def download_invoice_pdf(
    invoice_id: int,
    company_id: int,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    invoice = get_invoice_by_id(invoice_id, company_id, current_owner.id, db)

    company = db.query(Company).filter(
        Company.id == company_id,
        Company.owner_id == current_owner.id
    ).first()

    customer = db.query(Customer).filter(
        Customer.id == invoice.customer_id,
        Customer.company_id == company_id
    ).first()

    file_path = generate_invoice_pdf(invoice, company, customer)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/pdf"
    )
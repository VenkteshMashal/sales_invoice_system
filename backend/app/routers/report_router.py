from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.security import get_current_owner
from app.models.owner import Owner
from app.services.report_service import (
    get_summary_report,
    get_payment_status_report,
    get_top_customers_report,
    get_product_sales_report
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/summary/company/{company_id}")
def summary_report(
    company_id: int,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return get_summary_report(company_id, current_owner.id, db)


@router.get("/payment-status/company/{company_id}")
def payment_status_report(
    company_id: int,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return get_payment_status_report(company_id, current_owner.id, db)


@router.get("/top-customers/company/{company_id}")
def top_customers_report(
    company_id: int,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return get_top_customers_report(company_id, current_owner.id, db)


@router.get("/product-sales/company/{company_id}")
def product_sales_report(
    company_id: int,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return get_product_sales_report(company_id, current_owner.id, db)
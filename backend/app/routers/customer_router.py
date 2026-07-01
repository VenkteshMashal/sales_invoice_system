from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.security import get_current_owner
from app.models.owner import Owner
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.services.customer_service import (
    create_customer,
    get_customers,
    get_customer_by_id,
    update_customer,
    delete_customer
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post("/company/{company_id}", response_model=CustomerResponse)
def add_customer(
    company_id: int,
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return create_customer(company_id, current_owner.id, customer_data, db)


@router.get("/company/{company_id}", response_model=list[CustomerResponse])
def view_customers(
    company_id: int,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return get_customers(company_id, current_owner.id, db)


@router.get("/{customer_id}/company/{company_id}", response_model=CustomerResponse)
def view_customer(
    customer_id: int,
    company_id: int,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return get_customer_by_id(customer_id, company_id, current_owner.id, db)


@router.put("/{customer_id}/company/{company_id}", response_model=CustomerResponse)
def edit_customer(
    customer_id: int,
    company_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return update_customer(customer_id, company_id, current_owner.id, customer_data, db)


@router.delete("/{customer_id}/company/{company_id}")
def remove_customer(
    customer_id: int,
    company_id: int,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return delete_customer(customer_id, company_id, current_owner.id, db)
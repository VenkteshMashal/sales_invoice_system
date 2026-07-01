from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.security import get_current_owner
from app.models.owner import Owner
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from app.services.company_service import (
    create_company,
    get_companies,
    get_company_by_id,
    update_company,
    delete_company
)

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


@router.post("/", response_model=CompanyResponse)
def add_company(
    company_data: CompanyCreate,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return create_company(company_data, current_owner.id, db)


@router.get("/", response_model=list[CompanyResponse])
def view_companies(
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return get_companies(current_owner.id, db)


@router.get("/{company_id}", response_model=CompanyResponse)
def view_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return get_company_by_id(company_id, current_owner.id, db)


@router.put("/{company_id}", response_model=CompanyResponse)
def edit_company(
    company_id: int,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return update_company(company_id, company_data, current_owner.id, db)


@router.delete("/{company_id}")
def remove_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return delete_company(company_id, current_owner.id, db)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.security import get_current_owner
from app.models.owner import Owner
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import (
    create_product,
    get_products,
    get_product_by_id,
    update_product,
    delete_product
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/company/{company_id}", response_model=ProductResponse)
def add_product(
    company_id: int,
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return create_product(company_id, current_owner.id, product_data, db)


@router.get("/company/{company_id}", response_model=list[ProductResponse])
def view_products(
    company_id: int,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return get_products(company_id, current_owner.id, db)


@router.get("/{product_id}/company/{company_id}", response_model=ProductResponse)
def view_product(
    product_id: int,
    company_id: int,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return get_product_by_id(product_id, company_id, current_owner.id, db)


@router.put("/{product_id}/company/{company_id}", response_model=ProductResponse)
def edit_product(
    product_id: int,
    company_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return update_product(product_id, company_id, current_owner.id, product_data, db)


@router.delete("/{product_id}/company/{company_id}")
def remove_product(
    product_id: int,
    company_id: int,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    return delete_product(product_id, company_id, current_owner.id, db)
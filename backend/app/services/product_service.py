from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.product import Product
from app.models.company import Company
from app.schemas.product import ProductCreate, ProductUpdate


def verify_company(company_id: int, owner_id: int, db: Session):
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.owner_id == owner_id
    ).first()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )

    return company


def create_product(company_id: int, owner_id: int, product_data: ProductCreate, db: Session):
    verify_company(company_id, owner_id, db)

    new_product = Product(
        company_id=company_id,
        product_name=product_data.product_name,
        unit=product_data.unit,
        price_per_unit=product_data.price_per_unit,
        description=product_data.description
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


def get_products(company_id: int, owner_id: int, db: Session):
    verify_company(company_id, owner_id, db)

    return db.query(Product).filter(
        Product.company_id == company_id
    ).all()


def get_product_by_id(product_id: int, company_id: int, owner_id: int, db: Session):
    verify_company(company_id, owner_id, db)

    product = db.query(Product).filter(
        Product.id == product_id,
        Product.company_id == company_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


def update_product(product_id: int, company_id: int, owner_id: int, product_data: ProductUpdate, db: Session):
    product = get_product_by_id(product_id, company_id, owner_id, db)

    update_data = product_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product


def delete_product(product_id: int, company_id: int, owner_id: int, db: Session):
    product = get_product_by_id(product_id, company_id, owner_id, db)

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}
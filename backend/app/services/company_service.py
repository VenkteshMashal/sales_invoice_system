from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate


def create_company(company_data: CompanyCreate, owner_id: int, db: Session):
    new_company = Company(
        owner_id=owner_id,
        company_name=company_data.company_name,
        address=company_data.address,
        phone=company_data.phone,
        email=company_data.email,
        state=company_data.state
    )

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company


def get_companies(owner_id: int, db: Session):
    return db.query(Company).filter(Company.owner_id == owner_id).all()


def get_company_by_id(company_id: int, owner_id: int, db: Session):
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


def update_company(company_id: int, company_data: CompanyUpdate, owner_id: int, db: Session):
    company = get_company_by_id(company_id, owner_id, db)

    update_data = company_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(company, key, value)

    db.commit()
    db.refresh(company)

    return company


def delete_company(company_id: int, owner_id: int, db: Session):
    company = get_company_by_id(company_id, owner_id, db)

    db.delete(company)
    db.commit()

    return {"message": "Company deleted successfully"}
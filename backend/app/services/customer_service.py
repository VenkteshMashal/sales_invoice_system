from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.customer import Customer
from app.models.company import Company
from app.schemas.customer import CustomerCreate, CustomerUpdate


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


def create_customer(company_id: int, owner_id: int, customer_data: CustomerCreate, db: Session):
    verify_company(company_id, owner_id, db)

    new_customer = Customer(
        company_id=company_id,
        customer_name=customer_data.customer_name,
        phone=customer_data.phone,
        email=customer_data.email,
        address=customer_data.address,
        city=customer_data.city,
        state=customer_data.state,
        pin_code=customer_data.pin_code,
        gst_number=customer_data.gst_number
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


def get_customers(company_id: int, owner_id: int, db: Session):
    verify_company(company_id, owner_id, db)

    return db.query(Customer).filter(
        Customer.company_id == company_id
    ).all()


def get_customer_by_id(customer_id: int, company_id: int, owner_id: int, db: Session):
    verify_company(company_id, owner_id, db)

    customer = db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.company_id == company_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    return customer


def update_customer(customer_id: int, company_id: int, owner_id: int, customer_data: CustomerUpdate, db: Session):
    customer = get_customer_by_id(customer_id, company_id, owner_id, db)

    update_data = customer_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)

    return customer


def delete_customer(customer_id: int, company_id: int, owner_id: int, db: Session):
    customer = get_customer_by_id(customer_id, company_id, owner_id, db)

    db.delete(customer)
    db.commit()

    return {"message": "Customer deleted successfully"}
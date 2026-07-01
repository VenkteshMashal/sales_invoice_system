from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.company import Company
from app.models.customer import Customer
from app.models.product import Product
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
from app.schemas.invoice import InvoiceCreate


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


def generate_invoice_number(company_id: int, db: Session):
    last_invoice = db.query(Invoice).filter(
        Invoice.company_id == company_id
    ).order_by(Invoice.id.desc()).first()

    if not last_invoice:
        return "INV-0001"

    last_number = int(last_invoice.invoice_number.split("-")[1])
    new_number = last_number + 1

    return f"INV-{new_number:04d}"


def create_invoice(company_id: int, owner_id: int, invoice_data: InvoiceCreate, db: Session):
    verify_company(company_id, owner_id, db)

    customer = db.query(Customer).filter(
        Customer.id == invoice_data.customer_id,
        Customer.company_id == company_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found for this company"
        )

    if not invoice_data.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invoice must have at least one item"
        )

    invoice_items = []
    sub_total = Decimal("0.00")

    for item in invoice_data.items:
        product = db.query(Product).filter(
            Product.id == item.product_id,
            Product.company_id == company_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {item.product_id} not found"
            )

        amount = Decimal(item.quantity) * Decimal(product.price_per_unit)
        sub_total += amount

        invoice_items.append({
            "product_id": product.id,
            "item_name": product.product_name,
            "quantity": item.quantity,
            "unit": product.unit,
            "price_per_unit": product.price_per_unit,
            "amount": amount
        })

    invoice_number = generate_invoice_number(company_id, db)

    new_invoice = Invoice(
        company_id=company_id,
        customer_id=invoice_data.customer_id,
        invoice_number=invoice_number,
        invoice_date=invoice_data.invoice_date,
        sub_total=sub_total,
        total_amount=sub_total,
        paid_amount=Decimal("0.00"),
        balance_amount=sub_total,
        payment_status="Unpaid"
    )

    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    for item in invoice_items:
        new_item = InvoiceItem(
            invoice_id=new_invoice.id,
            product_id=item["product_id"],
            item_name=item["item_name"],
            quantity=item["quantity"],
            unit=item["unit"],
            price_per_unit=item["price_per_unit"],
            amount=item["amount"]
        )
        db.add(new_item)

    db.commit()
    db.refresh(new_invoice)

    return new_invoice


def get_invoices(company_id: int, owner_id: int, db: Session):
    verify_company(company_id, owner_id, db)

    return db.query(Invoice).filter(
        Invoice.company_id == company_id
    ).all()


def get_invoice_by_id(invoice_id: int, company_id: int, owner_id: int, db: Session):
    verify_company(company_id, owner_id, db)

    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.company_id == company_id
    ).first()

    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )

    return invoice
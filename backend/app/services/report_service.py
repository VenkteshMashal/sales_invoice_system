from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.company import Company
from app.models.invoice import Invoice
from app.models.customer import Customer
from app.models.invoice_item import InvoiceItem


def verify_company(company_id: int, owner_id: int, db: Session):
    return db.query(Company).filter(
        Company.id == company_id,
        Company.owner_id == owner_id
    ).first()


def get_summary_report(company_id: int, owner_id: int, db: Session):
    company = verify_company(company_id, owner_id, db)

    if not company:
        return {"message": "Company not found"}

    total_sales = db.query(func.coalesce(func.sum(Invoice.total_amount), 0)).filter(
        Invoice.company_id == company_id
    ).scalar()

    total_received = db.query(func.coalesce(func.sum(Invoice.paid_amount), 0)).filter(
        Invoice.company_id == company_id
    ).scalar()

    total_balance = db.query(func.coalesce(func.sum(Invoice.balance_amount), 0)).filter(
        Invoice.company_id == company_id
    ).scalar()

    total_invoices = db.query(func.count(Invoice.id)).filter(
        Invoice.company_id == company_id
    ).scalar()

    return {
        "total_sales": total_sales,
        "total_received": total_received,
        "total_balance": total_balance,
        "total_invoices": total_invoices
    }


def get_payment_status_report(company_id: int, owner_id: int, db: Session):
    verify_company(company_id, owner_id, db)

    result = db.query(
        Invoice.payment_status,
        func.count(Invoice.id)
    ).filter(
        Invoice.company_id == company_id
    ).group_by(
        Invoice.payment_status
    ).all()

    return [
        {"payment_status": status, "count": count}
        for status, count in result
    ]


def get_top_customers_report(company_id: int, owner_id: int, db: Session):
    verify_company(company_id, owner_id, db)

    result = db.query(
        Customer.customer_name,
        func.sum(Invoice.total_amount).label("total_purchase")
    ).join(
        Invoice, Invoice.customer_id == Customer.id
    ).filter(
        Invoice.company_id == company_id
    ).group_by(
        Customer.customer_name
    ).order_by(
        func.sum(Invoice.total_amount).desc()
    ).all()

    return [
        {"customer_name": name, "total_purchase": total}
        for name, total in result
    ]


def get_product_sales_report(company_id: int, owner_id: int, db: Session):
    verify_company(company_id, owner_id, db)

    result = db.query(
        InvoiceItem.item_name,
        func.sum(InvoiceItem.quantity).label("total_quantity"),
        func.sum(InvoiceItem.amount).label("total_amount")
    ).join(
        Invoice, Invoice.id == InvoiceItem.invoice_id
    ).filter(
        Invoice.company_id == company_id
    ).group_by(
        InvoiceItem.item_name
    ).order_by(
        func.sum(InvoiceItem.amount).desc()
    ).all()

    return [
        {
            "item_name": name,
            "total_quantity": quantity,
            "total_amount": amount
        }
        for name, quantity, amount in result
    ]
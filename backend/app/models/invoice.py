from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, Date
from sqlalchemy.orm import relationship
from datetime import datetime, date

from app.database.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    invoice_number = Column(String(50), nullable=False)
    invoice_date = Column(Date, default=date.today)

    sub_total = Column(Numeric(12, 2), nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)

    paid_amount = Column(Numeric(12, 2), default=0)
    balance_amount = Column(Numeric(12, 2), nullable=False)

    payment_status = Column(String(20), default="Unpaid")

    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete")
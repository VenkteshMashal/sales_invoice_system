from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Numeric
from datetime import datetime

from app.database.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    product_name = Column(String(150), nullable=False)
    unit = Column(String(50), nullable=False)
    price_per_unit = Column(Numeric(10, 2), nullable=False)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
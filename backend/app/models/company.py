from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=False)

    company_name = Column(String(150), nullable=False)
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(150))
    state = Column(String(100))

    owner = relationship("Owner", back_populates="companies")
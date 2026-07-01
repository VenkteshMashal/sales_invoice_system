from fastapi import FastAPI

from app.database.database import Base
from app.database.session import engine
from app.models import owner, company, customer, product, invoice, invoice_item
from app.routers import owner_router, company_router, customer_router, product_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sales Invoice Management System")

app.include_router(owner_router.router)
app.include_router(company_router.router)
app.include_router(customer_router.router)
app.include_router(product_router.router)

@app.get("/")
def home():
    return {"message": "Sales Invoice System API is running"}
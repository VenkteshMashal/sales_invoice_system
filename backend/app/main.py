from fastapi import FastAPI

from app.database.database import Base
from app.database.session import engine
from app.models import owner, company
from app.routers import owner_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Multi-Tenant Sales Invoice Management System")

app.include_router(owner_router.router)


@app.get("/")
def home():
    return {"message": "Sales Invoice System API is running"}
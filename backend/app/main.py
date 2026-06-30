from fastapi import FastAPI
from .database import engine, Base
from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Multi-Tenant Sales Invoice Management System")

@app.get("/")
def home():
    return {"message": "Sales Invoice System API is running"}
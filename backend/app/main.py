from fastapi import FastAPI

app = FastAPI(title="Sales Invoice Management System")

@app.get("/")
def home():
    return {"message": "Sales Invoice System API is running"}
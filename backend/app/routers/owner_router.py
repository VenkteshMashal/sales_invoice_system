from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.owner import OwnerRegister, OwnerLogin, OwnerResponse, TokenResponse
from app.services.owner_service import register_owner, authenticate_owner
from app.core.security import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=OwnerResponse)
def register(owner_data: OwnerRegister, db: Session = Depends(get_db)):
    return register_owner(owner_data, db)


@router.post("/login", response_model=TokenResponse)
def login(owner_data: OwnerLogin, db: Session = Depends(get_db)):
    owner = authenticate_owner(
        owner_data.email,
        owner_data.password,
        db
    )

    if not owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token(
        data={"sub": owner.email, "owner_id": owner.id}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
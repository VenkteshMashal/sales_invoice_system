from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.owner import Owner
from app.schemas.owner import OwnerRegister
from app.core.security import hash_password, verify_password


def register_owner(owner_data: OwnerRegister, db: Session):
    existing_owner = db.query(Owner).filter(
        Owner.email == owner_data.email
    ).first()

    if existing_owner:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_owner = Owner(
        owner_name=owner_data.owner_name,
        email=owner_data.email,
        password=hash_password(owner_data.password)
    )

    db.add(new_owner)
    db.commit()
    db.refresh(new_owner)

    return new_owner


def authenticate_owner(email: str, password: str, db: Session):
    owner = db.query(Owner).filter(Owner.email == email).first()

    if not owner:
        return None

    if not verify_password(password, owner.password):
        return None

    return owner
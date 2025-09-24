# app/services/portfolio_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.schemas.portfolio import PortfolioCreate, PortfolioOut
from app.services.portfolio_repository import create as repo_create

def create_portfolio(db: Session, user_id: int, payload: PortfolioCreate) -> PortfolioOut:
    try:
        obj = repo_create(
            db,
            user_id=user_id,
            name=payload.name,
            description=payload.description,
            currency=payload.currency,
        )
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Portfolio name already exists for this user",
        )

    db.refresh(obj)  # asegura ids/timestamps
    return PortfolioOut.model_validate(obj)  # Pydantic v2 (from_attributes=True)

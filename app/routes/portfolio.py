# app/routes/portfolios.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# from app.db.session import get_db
from app.schemas.portfolio import PortfolioCreate, PortfolioOut
from app.core.deps import get_current_user, get_db  # tu helper en deps
from app.services.portfolio_service import create_portfolio as create_portfolio_service




router = APIRouter()

@router.post("/", response_model=PortfolioOut, status_code=status.HTTP_201_CREATED)
def create_portfolio_endpoint(
    payload: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    user_id = current_user.user_id  # o current_user.id según tu deps
    return create_portfolio_service(db, user_id, payload)


# app/routes/portfolios.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# from app.db.session import get_db
from app.schemas.portfolio import PortfolioCreate, PortfolioOut
from app.core.deps import get_current_user, get_db  # tu helper en deps
from app.services.portfolio_service import create_portfolio as create_portfolio_service, get_portfolio_snapshot, take_portfolio_snapshot




router = APIRouter()
# TODO: Averiguar pq PortfolioCreate es obligatorio y donde se configura
@router.post("/", response_model=PortfolioOut, status_code=status.HTTP_201_CREATED)
def create_portfolio_endpoint(
    payload: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    user_id = current_user.user_id  # o current_user.id según tu deps
    return create_portfolio_service(db, user_id, payload)


@router.get("/{id:int}", response_model=PortfolioOut, status_code=status.HTTP_201_CREATED)
def get_portfolio(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    out = get_portfolio_snapshot(db, id)
    return out

@router.post("/snapshot/{id:int}", response_model=PortfolioOut, status_code=status.HTTP_201_CREATED)
def create_portfolio_snapshot(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return take_portfolio_snapshot(db, id)



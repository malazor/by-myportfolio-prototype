# app/repository/portfolio_repository.py
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.portfolio import Portfolio


def get_by_id(db: Session, portfolio_id: int) -> Optional[Portfolio]:
    stmt = select(Portfolio).where(Portfolio.portfolio_id == portfolio_id)
    return db.execute(stmt).scalar_one_or_none()

def is_owned_by_user(db: Session, portfolio_id: int, user_id: int) -> Optional[Portfolio]:
    stmt = select(Portfolio).where((Portfolio.portfolio_id == portfolio_id) & (Portfolio.user_id == user_id))
    return db.execute(stmt).scalar_one_or_none()


def get_by_user_and_name(db: Session, user_id: int, name: str) -> Optional[Portfolio]:
    stmt = (
        select(Portfolio)
        .where((Portfolio.user_id == user_id) & (Portfolio.name == name))
        .limit(1)
    )
    return db.execute(stmt).scalar_one_or_none()


def create(
    db: Session, *, user_id: int, name: str, description: str, currency: str
) -> Portfolio:
    obj = Portfolio(
        user_id=user_id,
        name=name,
        description=description,
        currency=currency,
        is_active=1,
    )
    db.add(obj)
    db.flush()
    return obj

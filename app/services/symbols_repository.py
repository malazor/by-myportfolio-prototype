# app/services/symbols_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.symbol import Symbol
from sqlalchemy import select
from app.models.v_asset_detail import VAssetDetail
from app.models.v_prices_daily import VPricesDaily
from typing import Optional
from datetime import date

def get_symbol_by_id(db: Session, id: int) -> Optional[Symbol]:
    return db.query(Symbol).filter(Symbol.id == id).first()

def get_symbol_by_symbol(db: Session, symbol: str) -> Optional[Symbol]:
    return db.query(Symbol).filter(Symbol.symbol == symbol).first()

def get_portfolio_symbol_by_symbol(db: Session, portfolio_id: int, symbol: str) -> Optional[VAssetDetail]:
    output = db.query(VAssetDetail).filter(VAssetDetail.symbol == symbol and VAssetDetail.portfolio_id == portfolio_id).first()
    return output

# TODO: Fusionar metodos Get History
def get_symbol_history_by_symbol(db: Session, id:int, symbol: str, start_date: date, end_date: date, order: str, limit: int) -> list[VPricesDaily]:
    stmt = (
        select(VPricesDaily)
    )

    if id:
        stmt = stmt.where(VPricesDaily.symbol_id == id)
    if symbol:
        stmt = stmt.where(VPricesDaily.symbol == symbol)
    if start_date:
        stmt = stmt.where(VPricesDaily.date >= start_date)
    if end_date:
        stmt = stmt.where(VPricesDaily.date <= end_date)

    if order=='desc':
        stmt = stmt.order_by(VPricesDaily.date.desc())

    if limit:
        stmt = stmt.limit(limit)
    print("Start date: ",start_date)
    print("End date: ",end_date)
    print(stmt)

    return db.execute(stmt).unique().scalars().all()

def get_last_price_by_id(db: Session, asset_id: int) -> list[VPricesDaily]:
    stmt = (
        select(VPricesDaily)
        .where(VPricesDaily.symbol_id == asset_id)
        .order_by(VPricesDaily.date.desc())
        .limit(1)
    )
    return db.execute(stmt).unique().scalars().all()


def find_symbols(
    db: Session,
    q: str | None = None,
    limit: int = 10,
    offset: int = 0,
    order_by: str = "symbol",
    order: str = "asc",
):
    query = db.query(Symbol)

    if q:
        pattern = f"%{q}%"
        query = query.filter(
            or_(
                Symbol.symbol.like(pattern),
                Symbol.short_name.like(pattern),
                Symbol.name.like(pattern),
            )
        )

    col_map = {
        "id": Symbol.id,
        "symbol": Symbol.symbol,
        "name": Symbol.name,
        "short_name": Symbol.short_name,
    }
    col = col_map.get(order_by, Symbol.symbol)
    query = query.order_by(col.asc() if order.lower() == "asc" else col.desc())

    total = query.count()
    items = query.offset(offset).limit(limit).all()
    return items, total

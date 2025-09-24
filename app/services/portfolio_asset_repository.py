# Solo firmas, sin implementar
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from datetime import date
from typing import Optional
from sqlalchemy import select
from app.models.portfolio_assets import PortfolioAssets  # usa tus nombres reales
from app.models.portfolio import Portfolio
from app.models.v_assets_portfolio import VPortfolioAssets
from app.models.assets import Assets

def get_portfolio_owned(db: Session, user_id: int, portfolio_id: int) -> Optional[Portfolio]:
    stmt = select(Portfolio).where((Portfolio.user_id == user_id) & (Portfolio.portfolio_id == portfolio_id)).limit(1)
#    return db.execute(stmt).scalar_one_or_none()
    output = db.execute(stmt)
    return output

def get_asset_by_id(db: Session, asset_id: int) -> Optional[Assets]:
    stmt = select(Assets).where(Assets.asset_id == asset_id).limit(1)
    return db.execute(stmt)

def list_assets_by_portfolio(db: Session, portfolio_id: int) -> list[VPortfolioAssets]:
    stmt = select(VPortfolioAssets).where(VPortfolioAssets.portfolio_id == portfolio_id)
    return db.execute(stmt).scalars().all()

def get_asset_by_symbol(db: Session, symbol: str) -> Optional[Assets]:
    stmt = select(Assets).where(Assets.symbol == symbol).limit(1)
    return db.execute(stmt)

def exists_portfolio_asset_pair(db: Session, portfolio_id: int, asset_id: int) -> bool: ...
def insert_portfolio_asset(
    db: Session,
    portfolio_id: int,
    asset_id: int,
    cantidad,
    precio_compra,
    fecha_compra: date,
) -> PortfolioAssets:
    obj = PortfolioAssets(
        portfolio_id=portfolio_id,
        asset_id=asset_id,
        cantidad=cantidad,
        precio_compra=precio_compra,
        fecha_compra=fecha_compra,
    )

    try:
        db.add(obj)
        db.flush()   # obtiene obj.id sin commitear
    except IntegrityError as e:
        print(e)
    finally:
        return obj
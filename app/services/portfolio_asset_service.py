# app/services/portfolio_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from datetime import datetime
from app.core.exceptions import NotFoundError, NotOwner, AlreadyExistsError
from app.core.mapping import to_dtos

from app.schemas.portfolio_assets import AddByIdOut, PortfolioAssetOut
from app.services.portfolio_asset_repository import insert_portfolio_asset, get_portfolio_owned, get_asset_by_id
from app.services.portfolio_asset_repository import list_assets_by_portfolio as svc_list_assets_by_portfolio
from app.services.portfolio_repository import get_by_id, is_owned_by_user


def add_asset_by_id(db, user_id, portfolio_id, dto, idempotency_key=None) -> AddByIdOut:
    try:

        if get_portfolio_owned(db, user_id, portfolio_id) is None:
            raise NotFoundError()
        else:
            if get_asset_by_id(db, dto.asset_id) is None:
                raise NotFoundError()
            else:
                obj = insert_portfolio_asset(
                db,
                portfolio_id= portfolio_id,
                asset_id= dto.asset_id,
                cantidad= dto.cantidad,
                precio_compra= dto.precio_compra,
                fecha_compra= datetime.today(),
                )
                db.commit()
    except IntegrityError:
        db.rollback()
        raise AlreadyExistsError(
            status_code=status.HTTP_409_CONFLICT,
            detail="Asset already exists for this portfolio",
        )
    db.refresh(obj)  # asegura ids/timestamps
    output = AddByIdOut.model_validate(obj)

    return output  # Pydantic v2 (from_attributes=True)

def list_assets_by_portfolio(db, portfolio_id: int, user_id: int) -> list[PortfolioAssetOut]:
    if get_by_id(db, portfolio_id) is None:
        raise NotFoundError()
    if not is_owned_by_user(db, portfolio_id, user_id):
        raise NotOwner()
    
    rows = svc_list_assets_by_portfolio(db, portfolio_id)
    return to_dtos(PortfolioAssetOut, rows)                      # list[DTO]



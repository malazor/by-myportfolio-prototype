# app/services/portfolio_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from datetime import datetime
from app.core.exceptions import NotFoundError, NotOwner, AlreadyExistsError, InvalidInput
from app.core.mapping import to_dtos

from app.schemas.portfolio_assets import AddByIdOut, PortfolioAssetOut, RemoveByIdOut
from app.services.portfolio_asset_repository import insert_portfolio_asset, get_portfolio_owned, get_asset_by_id, delete_portfolio_asset
from app.services.portfolio_asset_repository import list_assets_by_portfolio as svc_list_assets_by_portfolio
from app.services.portfolio_repository import get_by_id, is_owned_by_user
from app.services.symbols_repository import get_last_price_by_id

# TODO: FIX. Error controlado cuando el asset ya esta asignado.
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
                precio_compra= get_last_price_by_id(db, dto.asset_id)[0].close,
                fecha_compra= datetime.today(),
                )
                db.commit()
    except IntegrityError:
        db.rollback()
        raise AlreadyExistsError(
            status_code=status.HTTP_409_CONFLICT,
            detail="Asset already exists for this portfolio",
        )
    except Exception as e:
        print(e)
        db.rollback()
    db.refresh(obj)  # asegura ids/timestamps
    output = AddByIdOut.model_validate(obj)

    return output  # Pydantic v2 (from_attributes=True)

def remove_asset_by_id(db, user_id, portfolio_id, dto, idempotency_key=None) -> RemoveByIdOut:
    try:
        if get_portfolio_owned(db, user_id, portfolio_id) is None:
            raise NotFoundError()

        if get_asset_by_id(db, dto.asset_id) is None:
            raise NotFoundError()

        obj = delete_portfolio_asset(
            db,
            portfolio_id=portfolio_id,
            asset_id=dto.asset_id,
        )
        if obj is None:
            # no existía la relación en portfolio_assets
            raise NotFoundError()

        output = RemoveByIdOut(
            portfolio_id=portfolio_id,
            asset_id=dto.asset_id,
            deleted=True,
        )

        db.commit()

    except IntegrityError:
        db.rollback()
        # Para delete no tiene sentido AlreadyExistsError:
        raise InvalidInput(detail="Database integrity error while deleting asset")

    # No hacer db.refresh(obj) después de un delete
    print(f"Asset: {obj.asset_id} removed from portfolio: {obj.portfolio_id}")
    return output


def list_assets_by_portfolio(db, portfolio_id: int, user_id: int) -> list[PortfolioAssetOut]:
    if get_by_id(db, portfolio_id) is None:
        raise NotFoundError()
    if not is_owned_by_user(db, portfolio_id, user_id):
        raise NotOwner()
    
    rows = svc_list_assets_by_portfolio(db, portfolio_id)
    return to_dtos(PortfolioAssetOut, rows)                      # list[DTO]



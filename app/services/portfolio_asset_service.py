# app/services/portfolio_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import PendingRollbackError

from fastapi import HTTPException, status
from datetime import datetime
from app.core.exceptions import NotFoundError, NotOwner, AlreadyExistsError, InvalidInput
from app.core.mapping import to_dtos

from app.schemas.portfolio_assets import AddByIdOut, PortfolioAssetOut, RemoveAssetOut
from app.schemas.assets import AssetDetailOut
from app.services.portfolio_asset_repository import insert_portfolio_asset, get_portfolio_owned, get_asset_by_id, delete_portfolio_asset
from app.services.portfolio_asset_repository import list_assets_by_portfolio as svc_list_assets_by_portfolio
from app.services.portfolio_repository import get_by_id, is_owned_by_user
from app.services.symbols_repository import get_last_price_by_id, get_portfolio_symbol_by_symbol, get_symbol_history_by_symbol, get_portfolio_symbol_by_id


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
    except NotFoundError:
        db.rollback()
        raise HTTPException(status_code=404, detail="Symbol not found")    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Asset already exists for this portfolio")    
    except PendingRollbackError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Asset already exists for this portfolio")    
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=501, detail="Error no controlado.")    
    db.refresh(obj)  # asegura ids/timestamps
    output = AddByIdOut.model_validate(obj)

    return output  # Pydantic v2 (from_attributes=True)

def remove_asset_by_id(db, user_id, portfolio_id, dto, idempotency_key=None) -> RemoveAssetOut:
    try:
        if get_portfolio_owned(db, user_id, portfolio_id) is None:
            raise NotFoundError    

        if get_asset_by_id(db, dto.asset_id) is None:
            raise NotFoundError    

        obj = delete_portfolio_asset(
            db,
            portfolio_id=portfolio_id,
            asset_id=dto.asset_id,
        )
        if obj is None:
            raise NotFoundError    

        output = RemoveAssetOut(
            portfolio_id=portfolio_id,
            asset_id=dto.asset_id,
            deleted=True,
        )

        db.commit()

    except NotFoundError:
        db.rollback()
        raise HTTPException(status_code=404, detail="Portfolio or symbol not found for user")    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Asset already exists for this portfolio")    
    except PendingRollbackError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Asset already exists for this portfolio")    
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=501, detail="Error no controlado.")    

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

# TODO: Mover a portfolio_asset
def get_asset_snapshot(db: Session, portfolio_id: int, symbol: str, asset_id: int) -> AssetDetailOut:
    output = {}
    header = {}
    body = {}
    history = []
#   TODO: Mejorar el modelamiento de los procesos de negocio. Obtener Snapshot pot symbolo o por ID
#   TODO: Mejorar el manejo de errores por not found

    try:
        if asset_id:
            item = get_portfolio_symbol_by_id(db, portfolio_id, asset_id)
        else:
            item = get_portfolio_symbol_by_symbol(db, portfolio_id, symbol)
        
        if item is None:
            raise NotFoundError()


        output["id"]=item.id
        header["symbol"]=item.symbol
        header["current_price"]=item.current_price
        header["entry_price"]=item.entry_price
        header["diff"]=item.diff
        header["trend"]=item.trend

        body["name"]=item.name
        body["exchange"]=item.exchange
        body["currency"]=item.currency
        body["market_tz"]=item.market_tz
        body["status"]=item.status
        body["country"]=item.country
        body["sector"]=item.sector
        body["industry"]=item.industry
        body["website"]=item.website
        body["quote_type"]=item.quote_type

# TODO: Parametrizar alcance del historial
        out = get_symbol_history_by_symbol(db,None,symbol,None,None,"desc", 10)
        if out:
            for r in out:
                history_dict = {
                    "date":r.date,
                    "open":r.open,
                    "close":r.close,
                    "high":r.high,
                    "low":r.low,
                    "volume":r.volume
                }
                history.append(history_dict)
        else:
            history = [{"open":0,"close":0,"high":0,"low":0,"volume":0}]
#        history: list[HeaderDict] = [
#        VPricesDaily.model_validate(r) for r in out
#        ]


        output["header"]=header
        output["body"]=body
        output["history"]=history

    except NotFoundError:
        raise HTTPException(status_code=404, detail="Symbol or portfolio not found for user.")
    except Exception as e:
        raise HTTPException(status_code=501, detail="Error no controlado.")
    return output


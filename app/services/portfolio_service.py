# app/services/portfolio_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.schemas.portfolio import PortfolioCreate, PortfolioOut
from app.services.portfolio_repository import create as repo_create, get_portfolio_by_id, create_portfolio_snapshot
from app.services.portfolio_asset_repository import list_assets_by_portfolio
from app.services.symbols_repository import get_symbol_history_by_symbol

from datetime import datetime

from dateutil.relativedelta import relativedelta

from app.util.stats import calculate_initial_market_value, calculate_ratio_sharpe, calculate_volatility, calculate_current_market_value



def create_portfolio(db: Session, user_id: int, payload: PortfolioCreate) -> PortfolioOut:
    try:
        obj = repo_create(
            db,
            user_id=user_id,
            name=payload.name,
            description=payload.description,
            currency=payload.currency,
            market_value_1=0,
            ratio_sharpe=0,
            volatility=0,
            market_value_2=0,
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

def get_portfolio_snapshot(db: Session, portfolio_id: int) -> PortfolioOut:
#   TODO: Mejorar el modelamiento de los procesos de negocio. Obtener Snapshot pot symbolo o por ID
#   TODO: Mejorar el manejo de errores por not found
    try:
        output = get_portfolio_by_id(db, portfolio_id)
    except Exception as e:
        print(e)
    return output

def take_portfolio_snapshot(db: Session, portfolio_id: int) -> PortfolioOut:
#   TODO: Mejorar el modelamiento de los procesos de negocio. Obtener Snapshot pot symbolo o por ID
#   TODO: Mejorar el manejo de errores por not found
    values = {}
    asset_list = []
    history_list = []
    history_dict = {}

    output=[]

    try:
        assets = list_assets_by_portfolio(db, portfolio_id)

        if assets:
            for i in assets:
                assets_dict = {
                    "id":i.asset_id,
                    "symbol":i.symbol,
                    "cantidad":i.cantidad,
                    "precio_compra":i.precio_compra
                }
                history = get_symbol_history_by_symbol(db,None,i.symbol,datetime.now() - relativedelta(years=3),datetime.now(),"asc", None)
                if history:
                    assets_dict["precio_actual"] = history[-1].close
                    for j in history:
                        history_record = {
                            "date":j.date,
                            "symbol": j.symbol,
                            "open": float(j.open),
                            "close": float(j.close),
                            "high": float(j.high),
                            "low": float(j.low),
                            "volume": float(j.volume)
                        }
                        history_list.append(history_record)
                    history_dict = {
                        "assets":i.symbol,
                        "history":history_list
                    }
                asset_list.append(assets_dict)
        values = {"assets":asset_list, "history":history_dict}

        update_values = {
            "market_value_1": calculate_initial_market_value(asset_list),
            "ratio_sharpe": calculate_ratio_sharpe(history_list),
            "volatility": calculate_volatility(history_dict)
            ,"market_value_2": calculate_current_market_value(asset_list),
        }

        out = create_portfolio_snapshot(db, portfolio_id, update_values)

        output = get_portfolio_by_id(db, portfolio_id)

    except Exception as e:
        print(e)
    return output


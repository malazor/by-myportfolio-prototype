from sqlalchemy.orm import Session
from typing import Tuple, List, Optional
from app.schemas.symbols import SymbolListQuery, SymbolDetailOut, HeaderDict, BodyDict, HistoryDict
from app.services.symbols_repository import find_symbols
from app.models.symbol import Symbol
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.symbols_repository import get_symbol_by_id, get_symbol_by_symbol, get_portfolio_symbol_by_symbol, get_symbol_history_by_symbol
from app.models.v_prices_daily import VPricesDaily

def get_symbol_detail_by_id(db: Session, id: int):
    item = get_symbol_by_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return item

def get_symbol_detail_by_symbol(db: Session, symbol: str):
    item = get_symbol_by_symbol(db, symbol)
    if not item:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return item

def list_symbols_service(db: Session, params: SymbolListQuery) -> Tuple[List[Symbol], int]:
    q: Optional[str] = params.q.strip() if params.q else None
    limit = params.limit
    offset = params.offset
    # (order_by/order los integramos después en el repo)
    items, total = find_symbols(db, q=q, limit=limit, offset=offset)
    return items, total

def get_symbol_snapshot(db: Session, portfolio_id: int, symbol: str) -> SymbolDetailOut:
    output = {}
    header = {}
    body = {}
    history = []
#   TODO: Mejorar el modelamiento de los procesos de negocio. Obtener Snapshot pot symbolo o por ID
#   TODO: Mejorar el manejo de errores por not found

    try:
        item = get_portfolio_symbol_by_symbol(db, portfolio_id, symbol)
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

        out = get_symbol_history_by_symbol(db,symbol)
        if out:
            for r in out:
                history_dict = {
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


    except Exception as e:
        print(e)
    return output


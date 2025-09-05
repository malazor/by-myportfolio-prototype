from sqlalchemy.orm import Session
from typing import Tuple, List, Optional
from app.schemas.symbols import SymbolListQuery
from app.services.symbols_repository import find_symbols
from app.models.symbol import Symbol
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.symbols_repository import get_symbol_by_id, get_symbol_by_symbol

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

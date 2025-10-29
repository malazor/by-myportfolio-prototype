from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_current_user, get_db
from app.schemas.symbols import SymbolListResponse, SymbolListQuery, SymbolDetailOut
from app.services.symbols_service import list_symbols_service

router = APIRouter()
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_current_user, get_db
from app.schemas.symbols import SymbolDetailOutOld
from app.services.symbols_service import (
    get_symbol_detail_by_id,
    get_symbol_detail_by_symbol, get_symbol_snapshot
)

router = APIRouter()

@router.get("/{id:int}", response_model=SymbolDetailOut, tags=["Symbols"])
def get_symbol_by_id_route(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return get_symbol_snapshot(db, id, None)

@router.get("/{symbol}", response_model=SymbolDetailOut, tags=["Symbols"])
def get_symbol_by_symbol_route(
    symbol: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    out = get_symbol_snapshot(db, current_user.portfolio_id, symbol)
    return out


@router.get("/", response_model=SymbolListResponse, tags=["Symbols"])
def list_symbols(
    q: str | None = None,
    limit: int = 10,
    offset: int = 0,
    order_by: str = "symbol",
    order: str = "asc",
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    params = SymbolListQuery(q=q, limit=limit, offset=offset, order_by=order_by, order=order)
    items, total = list_symbols_service(db, params)
    return SymbolListResponse(items=items, total=total, limit=limit, offset=offset)


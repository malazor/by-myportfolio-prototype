# app/routes/temp_prices.py
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core import deps
from app.models.users import User 
from datetime import date
from app.db.crud.prices import get_by_symbol_and_date_range

router = APIRouter()
limit = None
offset = 0

@router.get("/prices", summary="Temporal: precios por símbolo y rango")
def get_prices(
    symbol: str,
    start: date,
    end: date,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    prices = get_by_symbol_and_date_range(
        db,
        symbol=symbol,
        start=start,
        end=end,
    )

    # si prices son Row -> convertir a dict
    prices_out = [dict(row._mapping) for row in prices]

    return {
        "symbol": symbol,
        "start": str(start),
        "end": str(end),
        "prices": prices_out,
    }
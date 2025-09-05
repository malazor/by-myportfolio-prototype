# app/db/crud/prices.py
from datetime import date
from sqlalchemy.orm import Session
from app.models.v_prices_daily import VPricesDaily

# TODO: Evaluar el manejo de la paginacion
def get_by_symbol_and_date_range(
    db: Session,
    *,
    symbol: str,
    start: date,
    end: date,
    limit: int | None = None,
    offset: int = 0,
):
    q = (
        db.query(
            VPricesDaily.date,
            VPricesDaily.open,
            VPricesDaily.high,
            VPricesDaily.low,
            VPricesDaily.close,
            VPricesDaily.volume,
        )
        .filter(
            VPricesDaily.symbol == symbol,
            VPricesDaily.date >= start,
            VPricesDaily.date <= end,
        )
        .order_by(VPricesDaily.date.asc())
        .offset(offset)
    )
    if limit:
        q = q.limit(limit)
    return q.all()

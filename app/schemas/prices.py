from datetime import date
from pydantic import BaseModel

class PriceItem(BaseModel):
    date: date
    open: float | None = None
    high: float | None = None
    low:  float | None = None
    close: float | None = None
    volume: int | None = None

class PricesOut(BaseModel):
    symbol: str
    start: date
    end: date
    count: int
    prices: list[PriceItem]

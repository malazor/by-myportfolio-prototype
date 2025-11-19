from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Literal

from datetime import date, datetime
from typing import Optional, Union
from pydantic import BaseModel, ConfigDict

from typing_extensions import TypedDict

class HeaderDict(TypedDict):
    symbol: str # Se obtiene de la tabla Symbol
    current_price: float # Se obtiene en linea
    entry_price: float # Se obtiene de la tabla
    diff: float  # e.g., "1.25%"
    trend: int

class BodyDict(TypedDict):
    name: str
    exchange: str
    currency: str
    market_tz: str
    status: str
    country: str
    sector: str
    industry: str
    website: str
    quote_type: str

class HistoryDict(TypedDict):
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int

class AssetDetailOut(BaseModel):
    id: int
    header: HeaderDict
    body: BodyDict
    history: list[HistoryDict]




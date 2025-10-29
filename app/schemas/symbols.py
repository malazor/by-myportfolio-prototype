from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Literal

from datetime import date, datetime
from typing import Optional, Union
from pydantic import BaseModel, ConfigDict

class SymbolDetailOutOld(BaseModel):
    id: int
    symbol: str
    name: Optional[str] = None
    short_name: Optional[str] = None
    asset_class: Optional[str] = None
    exchange: Optional[str] = None
    currency: Optional[str] = None
    market_tz: Optional[str] = None
    status: Optional[str] = None
    country: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    quote_type: Optional[str] = None
    first_seen: Optional[date] = None
    last_seen: Optional[date] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    meta: Optional[Union[dict, str]] = None  # si la BD guarda JSON como texto

    model_config = ConfigDict(from_attributes=True)

class SymbolOut(BaseModel):
    id: int
    symbol: str
    short_name: Optional[str] = None
    name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)  # <- clave en v2

class SymbolListResponse(BaseModel):
    items: List[SymbolOut]
    total: int
    limit: int
    offset: int

class SymbolListQuery(BaseModel):
    q: Optional[str] = None
    limit: int = Field(10, ge=1, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["id", "symbol", "name", "short_name"] = "symbol"
    order: Literal["asc", "desc"] = "asc"

from typing import TypedDict

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
    open: float
    high: float
    low: float
    close: float
    volume: int

class SymbolDetailOut(BaseModel):
    id: int
    header: HeaderDict
    body: BodyDict
    history: list[HistoryDict]




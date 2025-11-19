# app/schemas/portfolio_assets.py
from pydantic import BaseModel, Field
from datetime import date
from pydantic import ConfigDict

class AddByIdOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    portfolio_id: int
    asset_id: int
    cantidad: float
    precio_compra: float
    fecha_compra: date

class AddByIdIn(BaseModel):
    asset_id: int = Field(gt=0)
    cantidad: float = Field(gt=0)

class RemoveBySymbolIn(BaseModel):
    symbol: str


class RemoveByIdIn(BaseModel):
    asset_id: int = Field(gt=0)

class RemoveAssetOut(BaseModel):
    asset_id: int = Field(gt=0)
    portfolio_id: int
    deleted: bool


class AddBySymbolIn(BaseModel):
    symbol: str
    cantidad: float = Field(gt=0)

class PortfolioAssetOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    portfolio_id: int
    name: str
    description: str
    currency: str
    is_active: bool = Field(default=True)
    asset_id: int
    symbol: str | None = None
    short_name: str | None = None
    industry: str | None = None
    sector: str | None = None
    quote_type: str
    cantidad: float
    precio_compra: float

class PortfolioAssetCreate(BaseModel):
    pass

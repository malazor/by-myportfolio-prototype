# v2 imports
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Optional, Annotated
from datetime import datetime

class PortfolioBase(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    description: Annotated[str, Field(min_length=1, max_length=255)]  # <- obligatoria
    currency: Annotated[str, Field(min_length=3, max_length=3)]    

    # v1 @validator(..., pre=True) -> v2 @field_validator(..., mode='before')
    @field_validator('currency', mode='before')
    @classmethod
    def normalize_currency(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip().upper()
        if len(v) != 3:
            raise ValueError('currency must be exactly 3 letters (ISO 4217)')
        if not v.isalpha():
            raise ValueError('currency must be letters A–Z')
        return v

    # v1 @root_validator -> v2 @model_validator(mode='after')
    @model_validator(mode='after')
    def _business_rules(self):
        if self.name and self.currency and self.name.upper() == self.currency:
            raise ValueError('name and currency cannot match')
        return self

    # v1 Config(orm_mode=True, extra='forbid') -> v2 ConfigDict
    model_config = ConfigDict(
        from_attributes=True,   # reemplaza orm_mode=True
        extra='forbid',
        populate_by_name=True,
    )

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioOut(PortfolioBase):
    portfolio_id: int
    user_id: int
    name: str
    description: str
    currency: str
    market_value: float
    ratio_sharpe: float
    volatility: float
    is_active: bool
    created_at: datetime
    updated_at: datetime    

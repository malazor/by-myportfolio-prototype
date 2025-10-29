# app/models/v_prices_daily.py
from sqlalchemy import Column, Integer, String, Date, Numeric, BigInteger

from app.db.base import Base

class VAssetDetail(Base):
    __tablename__ = "v_asset_detail"
    __table_args__ = {'info': {'skip_autogenerate': True}}

    # 👇 Definimos columnas explícitamente si prefieres evitar autoload
    id  = Column(Integer)
    portfolio_id   = Column(BigInteger)
    asset_id  = Column(Integer)
    symbol     = Column(String(64))
    current_price = Column(Numeric(18,6))
    entry_price       = Column(Numeric(18,6))
    diff = Column(Numeric(18,6))
    trend = Column(Numeric(18,6))

    name = Column(String(255))
    exchange = Column(String(255))
    currency = Column(String(3))
    market_tz = Column(String(64))
    status = Column(String(8))
    country = Column(String(100))
    sector = Column(String(100))
    industry = Column(String(100))
    website = Column(String(100))
    quote_type = Column(String(50))

    # ⚠️ Nota: las vistas no tienen PK real
    __mapper_args__ = {
        "primary_key": [id, portfolio_id, asset_id]  # PK lógico
    }

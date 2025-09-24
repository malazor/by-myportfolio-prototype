# app/models/v_prices_daily.py
from sqlalchemy import Column, Integer, String, Date, Numeric, BigInteger, Boolean

from app.db.base import Base

class VPortfolioAssets(Base):
    __tablename__ = "v_assets_portfolio"
    __table_args__ = {'info': {'skip_autogenerate': True}}

    # 👇 Definimos columnas explícitamente si prefieres evitar autoload
    id   = Column(BigInteger(), primary_key=True)
    portfolio_id  = Column(BigInteger())
    name = Column(String(20))
    description = Column(String(20))
    currency = Column(String(3))
    is_active = Column(Boolean, nullable=False)
    asset_id = Column(Integer())
    symbol     = Column(String(64))
    short_name = Column(String(100))
    industry = Column(String(100))
    sector = Column(String(100))
    quote_type  = Column(String(50))
    cantidad        = Column(Numeric(18,6))
    precio_compra      = Column(Numeric(18,6))


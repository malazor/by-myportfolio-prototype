# app/models/portfolio.py
from sqlalchemy import (
    Column, BigInteger, String, Text, CHAR, TIMESTAMP, Integer, Numeric,
    ForeignKey, UniqueConstraint, text
)
from app.db.base import Base

class PortfolioAssets(Base):
    __tablename__ = "portfolio_assets"
    __table_args__ = (
        UniqueConstraint("portfolio_id", "asset_id", name="uq_portfolio_asset"),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    portfolio_id = Column(BigInteger, ForeignKey("portfolios.portfolio_id", ondelete="CASCADE"), nullable=False)
    asset_id = Column(BigInteger, ForeignKey("symbols.id", ondelete="CASCADE"), nullable=False)


    cantidad = Column(Integer, nullable=False, server_default=text("0"))  
    precio_compra = Column(Numeric(10, 2), nullable=False, server_default=text("0.00"))

    fecha_compra = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

# app/models/portfolio.py
from sqlalchemy import (
    Column, BigInteger, String, Text, CHAR, TIMESTAMP, Integer, Numeric, SmallInteger, Enum,
    ForeignKey, UniqueConstraint, text
)
from app.db.base import Base

class Assets(Base):
    __tablename__ = "assets"
    __table_args__ = (
        UniqueConstraint("symbol", name="uq_symbol"),
    )

    asset_id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    symbol = Column(String(20), nullable=False)
    name = Column(String(255), nullable=False)
    asset_type = Column(Enum("stock", "bond", "etf", "crypto", "commodity", "index", "forex", name="estado_enum"), nullable=False)
    currency = Column(CHAR(3), nullable=False, server_default="USD")
    exchange = Column(String(50), nullable=False)
    sector = Column(String(100), nullable=False)
    industry = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_Active = Column(SmallInteger, nullable=False, server_default="0")  # Mapea a TINYINT en MySQL

    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


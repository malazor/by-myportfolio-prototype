# app/models/symbol.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Date, Text, TIMESTAMP

from app.db.base import Base

# from sqlalchemy.orm import declarative_base

class Symbol(Base):
    __tablename__ = "symbols"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(64), nullable=False, unique=True)
    name = Column(String(255))
    short_name = Column(String(100))
    asset_class = Column(String(16))
    exchange = Column(String(64))
    currency = Column(String(3))
    market_tz = Column(String(64))
    status = Column(String(8))          # enum('active','inactive') en BD
    first_seen = Column(Date)
    last_seen = Column(Date)
    meta = Column(Text)                 # JSON validado en BD
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    country = Column(String(100))
    sector = Column(String(100))
    industry = Column(String(100))
    website = Column(String(100))
    quote_type = Column(String(50))

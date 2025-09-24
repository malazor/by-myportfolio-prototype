# app/models/v_prices_daily.py
from sqlalchemy import Column, Integer, String, Date, Numeric, BigInteger

from app.db.base import Base

class VPricesDaily(Base):
    __tablename__ = "v_prices_daily"
    __table_args__ = {'info': {'skip_autogenerate': True}}

    # 👇 Definimos columnas explícitamente si prefieres evitar autoload
    price_id   = Column(BigInteger)
    symbol_id  = Column(Integer)
    symbol     = Column(String(15))
    date       = Column(Date)
    open       = Column(Numeric(18,6))
    high       = Column(Numeric(18,6))
    low        = Column(Numeric(18,6))
    close      = Column(Numeric(18,6))
    volume     = Column(BigInteger)

    # ⚠️ Nota: las vistas no tienen PK real
    __mapper_args__ = {
        "primary_key": [symbol_id, date]  # PK lógico
    }

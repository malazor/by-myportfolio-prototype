# app/models/portfolio.py
from sqlalchemy import (
    Column, BigInteger, String, Text, CHAR, TIMESTAMP,
    ForeignKey, UniqueConstraint, text
)
from app.db.base import Base

class Portfolio(Base):
    __tablename__ = "portfolios"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_portfolios_user_name"),
    )

    portfolio_id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    name = Column(String(255), nullable=False)
    description = Column(Text)

    currency = Column(CHAR(3), nullable=False, server_default=text("'USD'"))
    is_active = Column(BigInteger, server_default=text("1"))  # TINYINT(1) en MySQL/MariaDB

    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

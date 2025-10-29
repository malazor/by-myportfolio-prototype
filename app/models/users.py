from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, BigInteger, String, Boolean, TIMESTAMP

from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    last_login = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

class UserAuth(Base):
    __tablename__ = "v_user_auth"
    user_id = Column(BigInteger)
    portfolio_id = Column(BigInteger, nullable=False)
    email = Column(String(255), nullable=False)
    username = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    password_hash = Column(String(255), nullable=False)

    __mapper_args__ = {
    "primary_key": [user_id, portfolio_id]
    }
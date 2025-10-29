from sqlalchemy.orm import Session
from app.models.users import User, UserAuth

def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_by_email_temp(db: Session, email: str) -> UserAuth | None:
    return db.query(UserAuth).filter(UserAuth.email == email).first()

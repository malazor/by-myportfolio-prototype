from sqlalchemy.orm import Session
from app.models.users import User

def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

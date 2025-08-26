from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.users import User
from app.core.security import decode_token

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")

# 👉 Manejo de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 👉 Obtener usuario actual desde el token
def get_current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)) -> User:
    try:
        payload = decode_token(token, verify_type="access")
        user_id = int(payload.get("sub"))
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

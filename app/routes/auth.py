# app/routes/auth.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.schemas.auth import Login
from app.core.security import create_access_token
from app.core.passwords import verify_password
from app.db.session import SessionLocal
from app.db.crud.user import get_by_email, get_by_email_temp
from app.core.security import create_access_token, decode_token, get_subject

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")

# TODO: Demo: usuario fijo (reemplaza por tu BBDD)
FAKE_USER = {"id": 1, "email": "manuel@test.com", "password": "123456", "name": "Manuel"}

# Lista negra simple (memoria) para logout
TOKEN_BLACKLIST: set[str] = set()

def get_current_payload(token: str = Depends(oauth2)):
    # Rechazar si está en blacklist
    if token in TOKEN_BLACKLIST:
        raise HTTPException(status_code=401, detail="Sesión cerrada")
    try:
        payload = decode_token(token, verify_type="access")
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

@router.post("/login")
def login(data: Login):
    with SessionLocal() as db:
#        user = get_by_email(db, data.email)
        user = get_by_email_temp(db, data.email)
        if not user or not user.is_active or not verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        token = create_access_token({"sub": str(user.user_id), "email": user.email, "portfolio_id": user.portfolio_id})
        return {"access_token": token, "token_type": "bearer", "user_id": user.user_id, "portfolio_id": user.portfolio_id}
    
@router.get("/me")
def me(current=Depends(get_current_payload)):
    return {"id": get_subject(current), "email": current.get("email")}

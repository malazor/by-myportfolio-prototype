from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.users import UserAuth
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
def get_current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)) -> UserAuth:
    try:
#        print("DEBUG: token recibido =>", token)

        payload = decode_token(token, verify_type="access")
#       print("DEBUG: payload decodificado =>", payload)

        user_id = payload.get("sub")
#       print("DEBUG: user_id en payload =>", user_id)

        if user_id is None:
            raise HTTPException(status_code=401, detail="El token no contiene 'sub'")
#       TODO: Esto es temporal, por el momento un solo usuario tiene un solo portafolio asignado.
#       user = db.query(User).filter(User.user_id == int(user_id)).first()
        user = db.query(UserAuth).filter(UserAuth.user_id == int(user_id)).first()
#       print("DEBUG: user encontrado en DB =>", user)

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        return user

    except Exception as e:
        print("DEBUG: excepción en get_current_user =>", str(e))
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

def get_current_user_dummy(token: str = Depends(oauth2)) -> UserAuth:
    return {"token_recibido": token}

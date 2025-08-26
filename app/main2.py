# main2.py
import argparse
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.passwords import hash_password
from app.db.session import SessionLocal
from app.models.users import User

def upsert_password(email: str, plain: str, create_if_missing: bool):
    h = hash_password(plain)
    with SessionLocal() as db:  # type: Session
        user = db.scalar(select(User).where(User.email == email))
        if user:
            user.password_hash = h
            db.commit()
            print(f"[OK] Password actualizado para {email}")
        else:
            if not create_if_missing:
                print(f"[X] Usuario no existe: {email}")
                return
            user = User(email=email, username=email, password_hash=h, is_active=True)
            db.add(user)
            db.commit()
            print(f"[OK] Usuario creado con hash para {email}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Set/Update user password hash")
    p.add_argument("--email", required=True)
    p.add_argument("--password", required=True)
    p.add_argument("--create", action="store_true", help="Crear usuario si no existe")
    args = p.parse_args()
    upsert_password(args.email, args.password, args.create)

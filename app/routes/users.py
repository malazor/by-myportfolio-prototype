from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.users import User
from app.core.security import decode_token
from app.core.deps import get_current_user_dummy
from app.core.deps import get_current_user

router = APIRouter()

# GET /users/{user_id}
@router.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.user_id,
        "email": current_user.email
    }

 # TODO: Implementar List Users
 # TODO: Implementar Get Users por ID o Symbol
 
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from typing import Optional, Dict, Any

from jose import jwt, JWTError

from app.core.config import settings  # lee .env vía config.py

# ========= Config =========
SECRET_KEY: str = settings.SECRET_KEY
ALGORITHM: str = getattr(settings, "ALGORITHM", "HS256")
ACCESS_MIN: int = int(getattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_DAYS: int = int(getattr(settings, "REFRESH_TOKEN_EXPIRE_DAYS", 7))
ISSUER: Optional[str] = getattr(settings, "JWT_ISSUER", None)
AUDIENCE: Optional[str] = getattr(settings, "JWT_AUDIENCE", None)


# ========= Helpers =========
def _now() -> datetime:
    return datetime.now(timezone.utc)


def _base_claims(extra: Dict[str, Any] | None = None) -> Dict[str, Any]:
    claims: Dict[str, Any] = {"iat": int(_now().timestamp()), "jti": str(uuid4())}
    if ISSUER:
        claims["iss"] = ISSUER
    if AUDIENCE:
        claims["aud"] = AUDIENCE
    if extra:
        claims.update(extra)
    return claims


# ========= Create Tokens =========
def create_access_token(data: Dict[str, Any], minutes: Optional[int] = None) -> str:
    exp_minutes = minutes if minutes is not None else ACCESS_MIN
    payload = _base_claims(
        {
            **data,
            "type": "access",
            "exp": _now() + timedelta(minutes=exp_minutes),
        }
    )
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: Dict[str, Any], days: Optional[int] = None) -> str:
    exp_days = days if days is not None else REFRESH_DAYS
    payload = _base_claims(
        {
            **data,
            "type": "refresh",
            "exp": _now() + timedelta(days=exp_days),
        }
    )
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ========= Decode / Validate =========
def decode_token(token: str, verify_type: Optional[str] = None, leeway: int = 30) -> Dict[str, Any]:
    """
    Decodifica y valida un token. Si verify_type se pasa ('access' o 'refresh'),
    valida que el claim 'type' coincida. 'leeway' agrega tolerancia de reloj (segundos).
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"leeway": leeway},
            audience=AUDIENCE if AUDIENCE else None,
            issuer=ISSUER if ISSUER else None,
        )
        if verify_type and payload.get("type") != verify_type:
            raise JWTError(f"Tipo de token inválido: se esperaba '{verify_type}'")
        return payload
    except JWTError as e:
        # En rutas, captura esta excepción y tradúcela a HTTP 401.
        raise e


def refresh_access_token(refresh_token: str) -> str:
    """
    Emite un nuevo access token a partir de un refresh token válido.
    """
    payload = decode_token(refresh_token, verify_type="refresh")
    # Evita propagar claims internos del token anterior
    data = {k: v for k, v in payload.items() if k not in {"exp", "type", "iat", "jti", "iss", "aud"}}
    return create_access_token(data)


def get_subject(payload: Dict[str, Any]) -> Optional[str]:
    """Devuelve el 'sub' (identificador de usuario) si existe."""
    return payload.get("sub")

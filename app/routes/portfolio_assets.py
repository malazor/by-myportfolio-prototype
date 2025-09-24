from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.core.exceptions import NotFound, NotOwner, AlreadyExistsError, InvalidInput
from app.schemas.portfolio_assets import AddByIdIn, AddBySymbolIn, PortfolioAssetOut, AddByIdOut
from app.services import portfolio_asset_service as svc

router = APIRouter(prefix="/{portfolio_id}/assets", tags=["PortfolioAssets"])

def map_error(e: Exception) -> HTTPException:
    if isinstance(e, svc.NotOwner):       return HTTPException(403, detail=str(e) or "No autorizado")
    if isinstance(e, svc.NotFoundError):       return HTTPException(404, detail=str(e) or "No encontrado")
    if isinstance(e, svc.AlreadyExistsError):  return HTTPException(409, detail=str(e) or "Ya existe")
    if isinstance(e, svc.IntegrityError):   return HTTPException(422, detail=str(e) or "Entrada inválida")
    return HTTPException(500, detail="Error interno")

@router.post("/by-id", response_model=AddByIdOut, status_code=status.HTTP_201_CREATED)
def add_by_id(portfolio_id: int,
              body: AddByIdIn,
              db: Session = Depends(get_db),
              user=Depends(get_current_user),
              idempotency_key: str | None = Header(None, alias="Idempotency-Key", convert_underscores=False)):
    try:
        output = svc.add_asset_by_id(db=db, user_id=user.user_id, portfolio_id=portfolio_id, dto=body, idempotency_key=idempotency_key)
        return output
    except Exception as e:
        raise map_error(e)

@router.post("/by-symbol", response_model=AddByIdOut, status_code=status.HTTP_201_CREATED)
def add_by_symbol(portfolio_id: int,
                  body: AddBySymbolIn,
                  db: Session = Depends(get_db),
                  user=Depends(get_current_user),
                  idempotency_key: str | None = Header(None, alias="Idempotency-Key", convert_underscores=False)):
    try:
        # Puedes implementar svc.add_asset_by_symbol o resolver symbol aquí y llamar add_asset_by_id
        # Por ahora, si ya tienes el service, llama directo:
        return svc.add_asset_by_symbol(db=db, user_id=user["id"], portfolio_id=portfolio_id, dto=body, idempotency_key=idempotency_key)
    except Exception as e:
        raise map_error(e)

@router.get("/", response_model=list[PortfolioAssetOut], status_code=status.HTTP_200_OK)
def list_assets(portfolio_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)):
    return svc.list_assets_by_portfolio(db, portfolio_id, user.user_id)

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.core.exceptions import NotFound, NotOwner, AlreadyExistsError, InvalidInput, NotFoundError
from app.schemas.portfolio_assets import AddByIdIn, AddBySymbolIn, PortfolioAssetOut, AddByIdOut, RemoveByIdIn, RemoveAssetOut, RemoveAssetOut, RemoveBySymbolIn
from app.schemas.assets import AssetDetailOut
from app.services import portfolio_asset_service as svc
from app.services import symbols_service as svc1


router = APIRouter(prefix="/{portfolio_id}/assets")

@router.post("/remove/by-id", response_model=RemoveAssetOut, status_code=status.HTTP_201_CREATED)
def remove_by_id(portfolio_id: int,
              body: RemoveByIdIn,
              db: Session = Depends(get_db),
              user=Depends(get_current_user),
              idempotency_key: str | None = Header(None, alias="Idempotency-Key", convert_underscores=False)):
    out = svc.remove_asset_by_id(db=db, user_id=user.user_id, portfolio_id=portfolio_id, dto=body, idempotency_key=idempotency_key)
    return out

@router.post("/remove/by-symbol", response_model=RemoveAssetOut, status_code=status.HTTP_201_CREATED)
def remove_by_symbol(portfolio_id: int,
              body: RemoveBySymbolIn,
              db: Session = Depends(get_db),
              user=Depends(get_current_user),
              idempotency_key: str | None = Header(None, alias="Idempotency-Key", convert_underscores=False)):
    symbol = svc1.get_symbol_detail_by_symbol(db, body.symbol)
    dto_body = body.model_copy(update={"asset_id": symbol.id})        

    out = svc.remove_asset_by_id(db=db, user_id=user.user_id, portfolio_id=portfolio_id, dto=dto_body, idempotency_key=idempotency_key)
    return out


@router.post("/add/by-id", response_model=AddByIdOut, status_code=status.HTTP_201_CREATED)
def add_by_id(portfolio_id: int,
              body: AddByIdIn,
              db: Session = Depends(get_db),
              user=Depends(get_current_user),
              idempotency_key: str | None = Header(None, alias="Idempotency-Key", convert_underscores=False)):
    output = svc.add_asset_by_id(db=db, user_id=user.user_id, portfolio_id=portfolio_id, dto=body, idempotency_key=idempotency_key)
    return output

@router.post("/add/by-symbol", response_model=AddByIdOut, status_code=status.HTTP_201_CREATED)
def add_by_symbol(portfolio_id: int,
                  body: AddBySymbolIn,
                  db: Session = Depends(get_db),
                  user=Depends(get_current_user),
                  idempotency_key: str | None = Header(None, alias="Idempotency-Key", convert_underscores=False)):
    symbol = svc1.get_symbol_detail_by_symbol(db, body.symbol)
    dto_body = body.model_copy(update={"asset_id": symbol.id})

    output = svc.add_asset_by_id(db=db, user_id=user.user_id, portfolio_id=portfolio_id, dto=dto_body, idempotency_key=idempotency_key)
    return output

@router.get("/", response_model=list[PortfolioAssetOut], status_code=status.HTTP_200_OK)
def list_assets(portfolio_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)):
    return svc.list_assets_by_portfolio(db, portfolio_id, user.user_id)

@router.get("/by-symbol/{symbol}", response_model=AssetDetailOut, status_code=status.HTTP_200_OK)
def get_asset_snapshot(portfolio_id: int,
    symbol:str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)):
    output = svc.get_asset_snapshot(db, portfolio_id, symbol, None)
    return output


@router.get("/by-id/{id}", response_model=AssetDetailOut, status_code=status.HTTP_200_OK)
def get_asset_snapshot(portfolio_id: int,
    id:int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)):
    output = svc.get_asset_snapshot(db, portfolio_id, None, id)
    return output        


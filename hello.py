from app.services.portfolio_asset_repository import list_assets_by_portfolio
from app.core.deps import get_db

print(list_assets_by_portfolio(get_db(), 5))



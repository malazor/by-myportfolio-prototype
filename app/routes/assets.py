from fastapi import APIRouter
import yfinance as yf

router = APIRouter()

# GET /assets/{symbol}
@router.get("/{symbol}")
def get_asset_price(symbol: str):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1d")

    if hist.empty:
        return {"error": f"No se encontró el símbolo {symbol}"}

    last_price = hist["Close"].iloc[-1]
    return {
        "symbol": symbol.upper(),
        "last_price": float(last_price)
    }

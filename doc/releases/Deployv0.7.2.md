# Mi API

## Autenticación

- Tipo: Bearer JWT
- Header: `Authorization: Bearer <token>`

## Endpoints

### GET /assets/{symbol}/detail

**Descripción:** Trae el detalle de un asset por su símbolo, asi como la data historica de los ultimos 7 días.  
**Query params:**
| nombre | tipo | req | descripción |
|---|---|---|---|
| symbol | string | sí | Ticker / Identificador (ej.: `AAPL`) |

**Headers:**

- `Authorization: Bearer <token>` _(requerido)_
- `Accept: application/json` _(recomendado)_

**Respuestas:**

- `200 OK`
  ```json
  {
    "id": 10,
    "header": {
      "symbol": "NVDA",
      "current_price": 201.029999,
      "entry_price": 190.96,
      "diff": 10.069999,
      "trend": 1
    },
    "body": {
      "name": "NVIDIA Corporation",
      "exchange": "NasdaqGS",
      "currency": "USD",
      "market_tz": "us_market",
      "status": "active",
      "country": "United States",
      "sector": "Technology",
      "industry": "Semiconductors",
      "website": "https://www.nvidia.com",
      "quote_type": "EQUITY"
    },
    "history": [
      {
        "open": 193.050003,
        "high": 203.149994,
        "low": 191.910004,
        "close": 201.029999,
        "volume": 295848900
      },
      {
        "open": 189.990005,
        "high": 192.0,
        "low": 188.429993,
        "close": 191.490005,
        "volume": 153452700
      },
      {
        "open": 183.839996,
        "high": 187.470001,
        "low": 183.5,
        "close": 186.259995,
        "volume": 131296700
      },
      {
        "open": 180.419998,
        "high": 183.029999,
        "low": 179.789993,
        "close": 182.160004,
        "volume": 111363700
      },
      {
        "open": 181.139999,
        "high": 183.440002,
        "low": 176.759995,
        "close": 180.279999,
        "volume": 162249600
      },
      {
        "open": 182.789993,
        "high": 182.789993,
        "low": 179.800003,
        "close": 181.160004,
        "volume": 124240200
      },
      {
        "open": 183.130005,
        "high": 185.199997,
        "low": 181.729996,
        "close": 182.639999,
        "volume": 128544700
      },
      {
        "open": 180.179993,
        "high": 184.100006,
        "low": 179.75,
        "close": 183.220001,
        "volume": 173135200
      },
      {
        "open": 182.229996,
        "high": 183.279999,
        "low": 179.770004,
        "close": 181.809998,
        "volume": 179723300
      },
      {
        "open": 184.800003,
        "high": 184.869995,
        "low": 177.289993,
        "close": 179.830002,
        "volume": 214450500
      }
    ]
  }
  ```

### Schemas:

- `SymbolDetailOut`

  ```python
    id: int
    header: HeaderDict
    body: BodyDict
    history: list[HistoryDict]
  ```

- `HeaderDict`

  ```python
    symbol: str
    current_price: float
    entry_price: float
    diff: str  # e.g., "1.25%"
    trend: str
  ```

- `BodyDict`

  ```python
    name: str
    exchange: str
    currency: str
    market_tz: str
    status: str
    country: str
    sector: str
    industry: str
    website: str
    quote_type: str
  ```

- `HistoryDict`

  ```python
    open: float
    high: float
    low: float
    close: float
    volume: int
  ```

### Vistas en DDBB

- `v_prices_daily`

  ```SQL
  create or replace
  algorithm = UNDEFINED view `portfolio`.`v_asset_detail` as
  SELECT
    s.id AS id,
    pa.portfolio_id AS portfolio_id,
    pa.asset_id AS asset_id,
    s.symbol AS symbol,
    v.max_close AS current_price,
    pa.precio_compra AS entry_price,
    (v.max_close - pa.precio_compra) AS diff,
  CASE
        WHEN v.max_close - pa.precio_compra > 0 THEN 1
        WHEN v.max_close - pa.precio_compra < 0 THEN -1
        ELSE 0
    END AS trend,
    s.name AS name,
    s.exchange AS exchange,
    s.currency AS currency,
    s.market_tz AS market_tz,
    s.status AS status,
    s.country AS country,
    s.sector AS sector,
    s.industry AS industry,
    s.website AS website,
    s.quote_type AS quote_type
  FROM
    portfolio.symbols s
  JOIN
    portfolio.portfolio_assets pa
    ON s.id = pa.asset_id  -- vínculo por activo
  LEFT JOIN (
    SELECT symbol_id, MAX(close) AS max_close
    FROM v_prices_daily
    GROUP BY symbol_id
  ) v
    ON v.symbol_id = s.id;
  ```

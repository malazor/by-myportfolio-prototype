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
  { "items": [{ "symbol": "AAPL", "name": "Apple Inc." }], "total": 1 }
  ```

### Schemas:

- `SymbolDetailOut`

  ```python
    id: int
    header: HeaderDict
    body: BodyDict
    history: HistoryDict
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

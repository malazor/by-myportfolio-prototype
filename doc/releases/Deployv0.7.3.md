# Mi API

## Autenticación

- Tipo: Bearer JWT
- Header: `Authorization: Bearer <token>`

## Endpoints

### GET /portfolio/{id}

**Descripción:** Trae el detalle de un portafolio por su id, asi como la lista de assets que lo compone.  
**Query params:**
N.A
**Headers:**

- `Authorization: Bearer <token>` _(requerido)_
- `Accept: application/json` _(recomendado)_

**Respuestas:**

### Schemas:

### DDBB

-- Se añade nueva columna market_value
ALTER TABLE portfolio.portfolios ADD market_value DECIMAL(18,6) NULL;
ALTER TABLE portfolio.portfolios ADD ratio_sharpe decimal(18,6) NULL;
ALTER TABLE portfolio.portfolios ADD volatility decimal(18,6) NULL;

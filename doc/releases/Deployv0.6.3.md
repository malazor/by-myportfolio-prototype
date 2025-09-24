# Deploy Add Porfolio

## 1. Modificaciones BBDD

### Modificaciones tabla portafolios

<pre>```
ALTER TABLE portfolios
  ADD CONSTRAINT uq_portfolios_user_name
  UNIQUE KEY (user_id, name);

```
</pre>

### Modificaciones tabla asset portafolios

<pre>
```
ALTER TABLE portfolio_assets
DROP CONSTRAINT fk_asset;

ALTER TABLE portfolio_assets
MODIFY COLUMN asset_id INT(10) UNSIGNED not null;

ALTER TABLE portfolio_assets
ADD CONSTRAINT fk_symbol
FOREIGN KEY (asset_id) REFERENCES symbols(id);

```
</pre>

### Creacion vista v_assets_portfolio

<pre>
```
create or replace
algorithm = UNDEFINED view `portfolio`.`v_assets_portfolio` as
select pa.id, pa.portfolio_id , p.name, p.description , p.currency , p.is_active ,
pa.asset_id , s.symbol,
 s.short_name , s.industry , s.sector , s.quote_type ,
pa.cantidad , pa.precio_compra
from portfolio_assets pa inner join portfolios p on pa.portfolio_id = p.portfolio_id 
inner join symbols s on s.id =pa.asset_id 

```</pre>

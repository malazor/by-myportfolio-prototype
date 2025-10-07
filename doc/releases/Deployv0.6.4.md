# Deploy Add Porfolio

## 1. Modificaciones BBDD

### Creacion vista v_user_auth

```sql
create or replace
algorithm = UNDEFINED view `portfolio`.`v_user_auth` as
select u.user_id, p.portfolio_id, u.email, u.username, u.is_active, u.password_hash
from users u inner join portfolios p on u.user_id =p.user_id
```

## Welcome to this Native App!

Please grant access to your *db.sch.tbl* table running the following SQL queries:

```
grant usage on database db to application role appn_role;
grant usage on schema db.sch to application role appn_role;
grant select, insert, update, delete on table db.sch.tbl to application role appn_role;
```
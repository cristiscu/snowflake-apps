use test.public;

select *
from test.public.customers_fake
limit 100;

select name, age
from test.public.customers_fake
order by age desc
limit 100;
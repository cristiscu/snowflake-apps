use test.public;

create or replace procedure test.public.gen_fake_rows_caller(r integer)
    returns Table()
    language python
    runtime_version = 3.9
    packages =('faker', 'snowflake-snowpark-python')
    handler = 'main'
    execute as caller       -- execute as owner by default!
as $$
import snowflake.snowpark as snowpark
from faker import Faker

# generate fake rows but with realistic test synthetic data
def main(session: snowpark.Session, rows: int):
    f = Faker()
    output = [[f.name(), f.address(), f.city(), f.state(), f.email()]
        for _ in range(rows)]
    
    schema = ["name", "address", "city", "state", "email"]
    df = session.create_dataframe(output, schema=schema)
    df.write.mode("overwrite").save_as_table("customers_fake")
    df.show()
    return df
$$;

call test.public.gen_fake_rows_caller(1000);

-- =======================================================
-- use w/ a different role!
create or replace role other_role;
grant role other_role to role accountadmin;

grant usage on database test to other_role;
grant usage on schema test.public to other_role;
grant usage on procedure test.public.gen_fake_rows_caller(integer) to other_role;
grant usage on warehouse compute_wh to other_role;

use role other_role;
call test.public.gen_fake_rows_caller(1000);

use role accountadmin;
grant all on table test.public.customers_fake to other_role;

use role other_role;
call test.public.gen_fake_rows_caller(1000);

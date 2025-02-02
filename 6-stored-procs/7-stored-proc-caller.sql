-- after Deploy > Open in Worksheets
-- see https://cristian-70480.medium.com/how-to-generate-snowflake-stored-procs-via-python-worksheets-01d49b5b3cb2

create procedure test.public.gen_fake_rows_c(rows integer)
    returns Table()
    language python
    runtime_version = 3.9
    packages =('faker', 'snowflake-snowpark-python')
    handler = 'main'
    execute as caller
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
    df.show()
    return df
$$;

-- use w/ different roles!
call test.public.gen_fake_rows_c(1000);
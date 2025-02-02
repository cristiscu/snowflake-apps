-- after Run. Then Query ID - Query Details

with PYTHON_WORKSHEET as procedure ()
    returns Table()
    language python
    runtime_version=3.9
    packages=('faker==18.9.0','snowflake-snowpark-python==*')
    handler='main'
as 'import snowflake.snowpark as snowpark
from faker import Faker
from random import randrange

# generates fake rows but with realistic test synthetic data
def main(session: snowpark.Session):
    f = Faker()
    output = [[f.name(), f.address(), f.city(), f.state(), f.email(), 10 + randrange(70)]
        for _ in range(1000)]

    schema = ["name", "address", "city", "state", "email", "age"]
    df = session.create_dataframe(output, schema=schema)
    df = df.filter("age < 20").update({"age": 20})
    df.show()
    return df'

call PYTHON_WORKSHEET();
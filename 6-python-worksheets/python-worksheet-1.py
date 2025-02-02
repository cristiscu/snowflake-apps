# copy and paste into a new Python Worksheet
# add faker to Packages (already included in Anaconda)

import snowflake.snowpark as snowpark
from faker import Faker
from random import randrange

# generate fake rows but with realistic test synthetic data
def main(session: snowpark.Session):
    f = Faker()
    output = [[f.name(), f.address(), f.city(), f.state(), f.email(), 10 + randrange(70)]
        for _ in range(1000)]
    
    schema = ["name", "address", "city", "state", "email", "age"]
    df = session.create_dataframe(output, schema=schema)
    df.show()
    return df
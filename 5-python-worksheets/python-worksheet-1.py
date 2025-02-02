# copy and paste into a new Python Worksheet
# add faker to Packages (already included in Anaconda)

import snowflake.snowpark as snowpark
from faker import Faker

# generate fake rows but with realistic test synthetic data
def main(session: snowpark.Session):
    f = Faker()
    output = [[f.name(), f.address(), f.city(), f.state(), f.email()]
        for _ in range(1000)]
    
    schema = ["name", "address", "city", "state", "email"]
    df = session.create_dataframe(output, schema=schema)
    df.show()
    return df
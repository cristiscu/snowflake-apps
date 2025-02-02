# run from a VSCode Terminal with "python 2-faker-to-table.py"

from faker import Faker
import os
import snowflake.snowpark as snowpark
from snowflake.snowpark import Session
from snowflake.snowpark.types import StructType, StructField, StringType
import warnings

warnings.filterwarnings("ignore")

def main(session: snowpark.Session, rows: int):
    f = Faker()
    output = [[f.name(), f.address(), f.city(), f.state(), f.email()]
        for _ in range(rows)]

    schema = StructType([ 
        StructField("NAME", StringType(), False),  
        StructField("ADDRESS", StringType(), False), 
        StructField("CITY", StringType(), False),  
        StructField("STATE", StringType(), False),  
        StructField("EMAIL", StringType(), False)
    ])
    df = session.create_dataframe(output, schema)
    df.write.mode("overwrite").save_as_table("customers_fake2")
    return df


pars = {
    "account": os.environ['SNOWFLAKE_ACCOUNT'],
    "user": os.environ['SNOWFLAKE_USER'],
    "password": os.environ['SNOWFLAKE_PASSWORD'],
    "database": "test",
    "schema": "public"
}
session = Session.builder.configs(pars).create()
main(session, 1000)

# show Snowpark DataFrame
query = 'select * from customers_fake2 limit 100'
session.sql(query).show()

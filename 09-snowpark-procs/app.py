from faker import Faker
import os
import snowflake.snowpark as snowpark
from snowflake.snowpark import Session, DataFrame
from snowflake.snowpark.types import StructType, StructField, StringType
from snowflake.snowpark.functions import sproc
import warnings

warnings.filterwarnings("ignore")
pars = {
    "account": os.environ['SNOWFLAKE_ACCOUNT'],
    "user": os.environ['SNOWFLAKE_USER'],
    "password": os.environ['SNOWFLAKE_PASSWORD'],
    "database": "test",
    "schema": "public"
}
session = Session.builder.configs(pars).create()

@sproc(name="gen_fake_rows_snowpark",
    replace=True,
    is_permanent=True,
    stage_location="@stage1",
    packages=["faker", "snowflake-snowpark-python"])
def main(session: snowpark.Session, rows: int) -> DataFrame:
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
    df.write.mode("overwrite").save_as_table("customers_fake")
    return df


#main(session, 1000)
session.sql("call gen_fake_rows_snowpark(1000)").show()

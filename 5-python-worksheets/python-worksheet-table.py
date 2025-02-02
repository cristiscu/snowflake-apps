# copy&paste into a new Python Worksheet in Snowsight
# select as context TEST.PUBLIC database+schema, and COMPUTE_WH warehouse
# add Faker in Packages popup
# Run --> new CUSTOMERS_FAKE2 table created, w/ 1K rows

import snowflake.snowpark as snowpark
from snowflake.snowpark.types import StructType, StructField, StringType
from faker import Faker

# generate fake rows but with realistic test synthetic data
def main(session: snowpark.Session):
    f = Faker()
    output = [[f.name(), f.address(), f.city(), f.state(), f.email()]
        for _ in range(1000)]

    schema = StructType([ 
        StructField("NAME", StringType(), False),  
        StructField("ADDRESS", StringType(), False), 
        StructField("CITY", StringType(), False),  
        StructField("STATE", StringType(), False),  
        StructField("EMAIL", StringType(), False)
    ])
    df = session.create_dataframe(output, schema)
    df.write.mode("overwrite").save_as_table("customers_fake2")
    df.show()
    return df

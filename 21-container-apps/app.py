# to be implemented as a job service

import streamlit as st
from faker import Faker
import os, sys, logging, warnings
from random import randrange
import matplotlib.pyplot as plt
from snowflake.snowpark import Session
from snowflake.snowpark.types import StructType, StructField, StringType, IntegerType

warnings.filterwarnings('ignore', category=UserWarning, module='snowflake.connector')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

st.title("Fake Data Generator")
st.caption("Generates fake and realistic data for a Customers table.")
logger.info('Started')

tableName = st.text_input("Enter the table name:", value="customers_fake")
if not st.button("Go"):
    st.stop()

params = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "database": "test",
    "schema": "public"
}
path = "/snowflake/session/token"
if os.path.exists(path):
    with open(path, "r") as f:
        params["authenticator"] = "oauth"
        params["token"] = f.read()
        params["host"] = os.getenv("SNOWFLAKE_HOST")
else:
    params["user"] = os.getenv("SNOWFLAKE_USER")
    params["password"] = os.getenv("SNOWFLAKE_PASSWORD")
session = Session.builder.configs(params).create()
logger.info('Connected')

f = Faker()
output = [[f.name(), f.address(), f.city(), f.state(), f.email(), 10 + randrange(70)]
    for _ in range(1000)]

schema = StructType([ 
    StructField("NAME", StringType(), False),  
    StructField("ADDRESS", StringType(), False), 
    StructField("CITY", StringType(), False),  
    StructField("STATE", StringType(), False),  
    StructField("EMAIL", StringType(), False),
    StructField("AGE", IntegerType(), False)
])
df = session.create_dataframe(output, schema)
df.write.mode("overwrite").save_as_table(tableName)
logger.info('Overwritten')

tabs = st.tabs(["Generated Data", "Queried Data"])
tabs[0].dataframe(df)

query = f'select * from {tableName} limit 100'
dfp = session.sql(query).to_pandas()
dfp.hist(column="AGE", bins=10)
tabs[1].pyplot(plt)
logger.info('Done')

# Run from a Terminal "streamlit run app.py", after "pip install streamlit"

import streamlit as st
from faker import Faker
import os
from random import randrange
import matplotlib.pyplot as plt
from snowflake.snowpark import Session
from snowflake.snowpark.types import StructType, StructField, StringType, IntegerType

st.title("Fake Data Generator")
st.caption("Generates fake and realistic data for a Customers table.")

tableName = st.text_input("Enter the table name:", value="customers_fake")
if not st.button("Go"):
    st.stop()

pars = {
    "account": os.environ['SNOWFLAKE_ACCOUNT'],
    "user": os.environ['SNOWFLAKE_USER'],
    "password": os.environ['SNOWFLAKE_PASSWORD'],
    "database": "test",
    "schema": "public"
}
session = Session.builder.configs(pars).create()

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

tabs = st.tabs(["Generated Data", "Queried Data"])
tabs[0].dataframe(df)

query = f'select * from {tableName} limit 100'
dfp = session.sql(query).to_pandas()
dfp.hist(column="AGE", bins=10)
tabs[1].pyplot(plt)

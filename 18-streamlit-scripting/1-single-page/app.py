import streamlit as st
from faker import Faker
import matplotlib.pyplot as plt
from random import randrange
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.types import StructType, StructField, StringType, IntegerType

st.title("Fake Data Generator")
st.caption("Generates fake and realistic data for a Customers table.")

tableName = st.text_input("Enter the table name:", value="customers_fake")
if not st.button("Go"):
    st.stop()

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
session = get_active_session()
df = session.create_dataframe(output, schema)
df.write.mode("overwrite").save_as_table(tableName)

tabs = st.tabs(["Generated Data", "Queried Data"])
tabs[0].dataframe(df)

# show Snowpark DataFrame
query = f'select * from {tableName} limit 100'
df = session.sql(query).to_pandas()
df.hist(column="AGE", bins=10)
tabs[1].pyplot(plt)

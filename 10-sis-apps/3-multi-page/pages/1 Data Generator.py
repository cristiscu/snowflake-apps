import streamlit as st
from faker import Faker
from snowflake.snowpark.types import StructType, StructField, StringType
from snowflake.snowpark.context import get_active_session
import utils

st.title("Fake Data Generator")
st.caption("Generates fake and realistic data for a Customers table.")

if not st.button("Go"): st.stop()

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
df = get_active_session().create_dataframe(output, schema)
df.write.mode("overwrite").save_as_table(utils.tableName)
st.write(f"Data below was saved in **{utils.tableName}**:")
st.dataframe(df)

import streamlit as st
from faker import Faker
from snowflake.snowpark.types import StructType, StructField, StringType
from snowflake.snowpark import Session
import utils

@st.cache_resource(max_entries=10)
def getSession(connection_name="snowflake"):
    section = st.secrets[f"connections_{connection_name}"]
    pars = {
        "account": section["account"],
        "user": section["user"],
        "password": section["password"],
        "database": "test",
        "schema": "public"
    }
    return Session.builder.configs(pars).create()


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
df = getSession().create_dataframe(output, schema)
df.write.mode("overwrite").save_as_table(utils.tableName)
st.write(f"Data below was saved in **{utils.tableName}**:")
st.dataframe(df)

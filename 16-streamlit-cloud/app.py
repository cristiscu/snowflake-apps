import streamlit as st
from faker import Faker
import matplotlib.pyplot as plt
from random import randrange
from snowflake.snowpark import Session
from snowflake.snowpark.types import StructType, StructField, StringType, IntegerType

st.title("Fake Data Generator and Inspector")
st.caption("Generates and reads back fake and realistic data for a Customers table.")

tabs = st.tabs(["Snowflake Connection", "Data Generator", "Data Inspector"])
with tabs[0]:
    with st.form("my-form"):
        account = st.text_input("Account:")
        user = st.text_input("User:")
        password = st.text_input("Password:", type="password")
        tableName = st.text_input("Table Name:", value="customers_fake")

        if not st.form_submit_button("Connect"):
            st.stop()

    pars = {
        "account": account,
        "user": user,
        "password": password,
        "database": "test",
        "schema": "public"
    }
    try:
        session = Session.builder.configs(pars).create()
        st.info("Connected to Snowflake.")
    except:
        st.error("Cannot connect to Snowflake!")
        st.stop()

with tabs[1]:
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
    st.dataframe(df)

with tabs[2]:
    query = f'select * from {tableName} limit 100'
    df = session.sql(query).to_pandas()
    df.hist(column="AGE", bins=10)
    st.pyplot(plt)

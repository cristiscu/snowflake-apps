import streamlit as st
from faker import Faker
from random import randrange
import matplotlib.pyplot as plt
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.types import StructType, StructField, StringType, IntegerType

st.title("Fake Data Generator")
st.caption("Generates fake and realistic data for a Customers table.")

tableName = st.text_input("Enter the table name:", value="customers_fake2")
if not st.button("Go"):
    st.stop()

# ==============================================
# check required object-level references
import snowflake.permissions as permission
ref = permission.get_reference_associations("customers_fake")
if len(ref) == 0:
    permission.request_reference("customers_fake")
    st.stop()
# ==============================================

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
customers_fake = "reference('customers_fake')"
df.write.mode("overwrite").save_as_table(customers_fake)

tabs = st.tabs(["Generated Data", "Queried Data"])
tabs[0].dataframe(df)

query = f'select * from {customers_fake} limit 100'
df = session.sql(query).to_pandas()
df.hist(column="AGE", bins=10)
tabs[1].pyplot(plt)

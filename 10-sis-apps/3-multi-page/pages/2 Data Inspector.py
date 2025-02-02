import streamlit as st
from snowflake.snowpark.context import get_active_session
import utils

st.title("Fake Data Inspector")
st.caption("Read back fake and realistic data generated for a Customers table.")

st.write(f"First 100 rows from **{utils.tableName}**:")
query = f"select * from {utils.tableName} limit 100"
df = get_active_session().sql(query)
st.dataframe(df)

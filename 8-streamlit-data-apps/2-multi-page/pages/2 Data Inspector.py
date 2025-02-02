import streamlit as st
import utils

st.title("Fake Data Inspector")
st.caption("Read back fake and realistic data generated for a Customers table.")

st.write(f"First 100 rows from **{utils.tableName}**:")
conn = st.connection("snowflake")
df = conn.query(f"select * from {utils.tableName} limit 100",
    ttl=3600, show_spinner="Running query...")
st.dataframe(df)

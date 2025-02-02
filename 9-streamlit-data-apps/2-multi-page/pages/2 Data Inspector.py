import streamlit as st
import matplotlib.pyplot as plt
import utils

st.title("Fake Data Inspector")
st.caption("Read back fake and realistic data generated for a Customers table.")

conn = st.connection("snowflake")
df = conn.query(f"select * from {utils.tableName} limit 100",
    ttl=3600, show_spinner="Running query...")
df.hist(column="AGE", bins=10)
st.pyplot(plt)

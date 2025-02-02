import streamlit as st
import matplotlib.pyplot as plt
from snowflake.snowpark.context import get_active_session
import utils

st.title("Fake Data Inspector")
st.caption("Read back fake and realistic data generated for a Customers table.")

query = f"select * from {utils.tableName} limit 100"
df = get_active_session().sql(query).to_pandas()
df.hist(column="AGE", bins=10)
st.pyplot(plt)

import streamlit as st
import pandas as pd
from faker import Faker
from random import randrange
import matplotlib.pyplot as plt
from snowflake.snowpark.context import get_active_session

st.title("Fake Data Generator")
st.caption("Generates fake and realistic data for a Customers table.")
tabG, tabQ = st.tabs(["Generated Data", "Queried Data"])

f = Faker()
output = [[f.name(), f.address(), f.city(), f.state(), f.email(), 10 + randrange(70)]
    for _ in range(1000)]

schema = ["name", "address", "city", "state", "email", "age"]
df = get_active_session().create_dataframe(output, schema)
tabG.dataframe(df)

df = pd.DataFrame(df.collect())
df.hist(column="age", bins=10)
tabQ.pyplot(plt)

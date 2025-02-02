import streamlit as st
import utils

st.title("Fake Data Generator and Inspector")
st.caption("Generates and reads back fake and realistic data for a Customers table.")

utils.tableName = st.text_input("Enter the table name:", value=utils.tableName)
st.info("Select one menu item from the left sidebar")
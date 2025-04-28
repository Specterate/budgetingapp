import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection


test_dict = {
    "0": {"name": "Alice", "age": 30, "location": "New York"},
    "1": {"name": "Bob", "age": 25, "location": "San Francisco"},
    "2": {"name": "Charlie", "age": 35, "location": "Chicago"},
    "3": {"name": "Diana", "age": 28, "location": "Seattle"}
}

test_df = pd.DataFrame.from_dict(test_dict, orient='index')

if "ss_df" not in st.session_state:
    st.session_state.ss_df = test_df.copy()

st.write("This is the session state")
st.session_state

with st.form("my_form", clear_on_submit=True, border=True):
    st.write("Inside the form")
    name = st.text_input("Name", placeholder="Enter your name")
    age = st.number_input("Age", min_value=0, max_value=100)
    location = st.selectbox("Location", ["New York", "San Francisco", "Chicago", "Seattle"])
    submitted = st.form_submit_button("Submit", type="primary")
    if submitted:
        new_row_df = pd.DataFrame.from_dict("0":{"name": name, "age": age, "location": location})
        test_df = pd.concat([df,new_row_df], ignore_index=True)
        st.success("Form submitted successfully!")        
    else:
        st.warning("Please fill out the form and submit.")
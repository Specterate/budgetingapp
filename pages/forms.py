import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection
from streamlit import session_state as ss


test_dict = {
    "0": {"name": "Alice", "age": 30, "location": "New York"},
    "1": {"name": "Bob", "age": 25, "location": "San Francisco"},
    "2": {"name": "Charlie", "age": 35, "location": "Chicago"},
    "3": {"name": "Diana", "age": 28, "location": "Seattle"}
}

test_df = pd.DataFrame.from_dict(test_dict, orient='index')

if "ss_df" not in st.session_state:
    st.ss.ss_df = test_df.copy()

st.write("This is the session state")
st.ss

def update_ss():
    new_row_df = pd.DataFrame.from_dict({"0":{"name": st.ss.name, "age": st.ss.age, "location": st.ss.location}})
    st.ss
    pass

with st.form("my_form", clear_on_submit=True, border=True):
        st.write("Inside the form")
        st.ss.name = st.text_input("Name", placeholder="Enter your name")
        st.ss.age = st.number_input("Age", min_value=0, max_value=100)
        st.ss.location = st.selectbox("Location", ["New York", "San Francisco", "Chicago", "Seattle"])
        submitted = st.form_submit_button("Submit", type="primary", on_click=update_ss)
        
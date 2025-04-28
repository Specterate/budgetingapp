import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection

# Create a test dictionary
test_dict = {
    "0": {"name": "Alice", "age": 30, "location": "New York"},
    "1": {"name": "Bob", "age": 25, "location": "San Francisco"},
    "2": {"name": "Charlie", "age": 35, "location": "Chicago"},
    "3": {"name": "Diana", "age": 28, "location": "Seattle"}
}

# convert the dictionary into a pandas dataframe
test_df = pd.DataFrame.from_dict(test_dict, orient='index')

# check if key exists in session state
if "ss_df" not in st.session_state:
    st.session_state.ss_df = test_df.copy()

with st.container:
    st.title("Data Preview")
    st.dataframe(st.session_state['ss_df'], hide_index=True)

def update_ss():
    new_row_df = pd.DataFrame.from_dict([{"name": st.session_state.name, "age": st.session_state.age, "location": st.session_state.location}])
    st.session_state.ss_df = pd.concat([st.session_state.ss_df, new_row_df], ignore_index=True)

def delete_ss():
    st.session_state.ss_df = st.session_state.ss_df[st.session_state.ss_df.name != st.session_state.delete_index]
    
col1, col2 = st.columns(2,border=True)
with col1:
    with st.form("my_form", clear_on_submit=True, border=True):
            st.write("Add new entry")
            # st.session_state.name = st.text_input("Name", placeholder="Enter your name")
            # st.session_state.age = st.number_input("Age", min_value=0, max_value=100)
            # st.session_state.location = st.selectbox("Location", ["New York", "San Francisco", "Chicago", "Seattle"])
            name = st.text_input("Name", placeholder="Enter your name", key="name")
            age = st.number_input("Age", min_value=0, max_value=100, key="age")
            location = st.selectbox("Location", ["New York", "San Francisco", "Chicago", "Seattle"], key="location")
            submitted = st.form_submit_button("Submit", type="primary", on_click=update_ss)
with col2:
    with st.form("delete_form", clear_on_submit=True, border=True):
        st.write("Delete entry")
        st.selectbox("Select entry to delete", st.session_state.ss_df.name.unique(), key="delete_index")
        st.form_submit_button("Delete", type="primary", on_click=delete_ss)
import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection, execute_query
import datetime
import pathlib
from openai import OpenAI

# Function to refresh the dashboard
def refresh_dashboard():
    for key in st.session_state.keys():
        if key != 'user_email':
            del st.session_state[key]

# Sidebar
with st.sidebar:
    st.button("Refresh Page", type="primary", use_container_width=True, on_click=refresh_dashboard)

if "user_email" not in st.session_state or st.session_state.user_email is None:
    st.write("User is not logged in")
    if st.button("Go to Login Page", type="primary"):
        # Redirect to login page
        st.switch_page("Budgetingapp.py")
else:
    # Set Supabase connection and session state
    if 'conn' not in st.session_state:
        conn = st.connection("supabase",type=SupabaseConnection)
        st.session_state.conn = conn

    get_transaction_data = st.button("Get Transaction Data", type="primary")
    if get_transaction_data:
        # set session state for get category data
        if 'get_transaction_data_for_open_ai_df' not in st.session_state:
            # Query categories table from supabase
            dictionary_data = st.session_state.conn.table("transactions").select("description", "subcategory").execute()
            st.session_state.get_transaction_data_for_open_ai_df = pd.DataFrame.from_dict(dictionary_data.data)
            print(dictionary_data.data)
            print(st.session_state.get_transaction_data_for_open_ai_df)

# 1 - Drop duplicates from the transaction data
# 2 - Feed the transaction data to Open AI and create a dictionary of descriptions and subcategories
# 3 - Feed this data to the supabase database to "category assignment"
# 4 - 

with st.expander("Session State", expanded=False):
    st.session_state
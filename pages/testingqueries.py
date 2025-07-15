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
import re

# Function to refresh the dashboard
def refresh_dashboard():
    for key in st.session_state.keys():
        print(f'key is {key}')
        if key != 'user_email' and key != 'user_id' and key != 'conn':
            print(f"Deleting key: {key}")
            del st.session_state[key]   

def clean_description(desc):
    desc = desc.lower()
    desc = re.sub(r'[^a-z0-9\s]', '', desc)  # Now keeps numbers!
    # Remove 'payment to' prefix if you want to focus on the merchant
    desc = re.sub(r'^payment to\s+', '', desc)
    desc = re.sub(r'\s+', ' ', desc).strip()
    # Optionally, remove trailing vendor codes, etc.
    tokens = desc.split()
    # If last token is not a vendor word, you could remove it:
    if len(tokens) > 2 and len(tokens[-1]) > 2 and tokens[-1].isalpha() is False:
        tokens = tokens[:-1]
    return ' '.join(tokens)

# Sidebar
with st.sidebar:
    st.button("Refresh Page", type="primary", use_container_width=True, on_click=refresh_dashboard)

if "user_email" not in st.session_state or st.session_state.user_email is None:
    st.write("User is not logged in")
    if st.button("Go to Login Page", type="primary"):
        # Redirect to login page
        st.switch_page("budgetingapp.py")
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
            print("before cleaning")
            print(st.session_state.get_transaction_data_for_open_ai_df)
    
        for index, row in st.session_state.get_transaction_data_for_open_ai_df.iterrows():
            # Clean the description
            cleaned_description = clean_description(row['description'])
            st.session_state.get_transaction_data_for_open_ai_df.at[index, 'description'] = cleaned_description

        print("after cleaning")
        print(st.session_state.get_transaction_data_for_open_ai_df)

        # Display the cleaned data
        st.write(st.session_state.get_transaction_data_for_open_ai_df)

# 1 - Drop duplicates from the transaction data
# 2 - Feed the transaction data to Open AI and create a dictionary of descriptions and subcategories
# 3 - Feed this data to the supabase database to "category assignment"

with st.expander("Session State", expanded=False):
    st.session_state
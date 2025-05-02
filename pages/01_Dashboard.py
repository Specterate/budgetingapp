import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection, execute_query

# set page configuration and title
st.set_page_config(page_title="Dashboard", page_icon="📊")
st.title("Dashboard")

if "user_email" not in st.session_state or st.session_state.user_email is None:
    st.write("User is not logged in")
    if st.button("Go to Login Page", type="primary"):
        # Redirect to login page
        st.switch_page("Budgettingapp.py")
else:
    # Set Supabase connection and session state
    if 'conn' not in st.session_state:
        conn = st.connection("supabase",type=SupabaseConnection)
        st.session_state.conn = conn

    
    # set session state for get data
    if 'get_category_data_df_ss' not in st.session_state:

        # Query categories table from supabase
        get_category_data = st.session_state.conn.table("categories").select("*").execute()

        # Convert get_data to pandas dataframe
        get_category_data_df = pd.DataFrame.from_dict(get_category_data.data)
        st.session_state.get_category_data_df_ss = get_category_data_df
        st.dataframe(st.session_state.get_category_data_df_ss, hide_index=True, use_container_width=True)
    
    col1, col2, col3 = st.columns(3, border=True)
    with col1:
        debit_sum = st.session_state.get_category_data_df_ss[st.session_state.get_category_data_df_ss['categorytype'] == 'Debit'].sum(numeric_only=True).astype(np.int64)
        st.write(f"Total Monthly Debit: ${debit_sum['monthly']}")
    with col2:
        credit_sum = st.session_state.get_category_data_df_ss[st.session_state.get_category_data_df_ss['categorytype'] == 'Credit'].sum(numeric_only=True).astype(np.int64)
        st.write(f"Total Monthly Credit: ${credit_sum['monthly']}")
    with col3:
        balance_sum = (credit_sum['monthly'] + debit_sum['monthly'])
        st.write(f"Total Monthly Balance: ${balance_sum}")

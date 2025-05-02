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
    if 'dashboard_get_category_data_df_ss' not in st.session_state:

        # Query categories table from supabase
        dashboard_get_category_data = st.session_state.conn.table("categories").select("*").execute()

        # Convert get_data to pandas dataframe
        dashboard_get_category_data_df = pd.DataFrame.from_dict(dashboard_get_category_data.data)
        st.session_state.dashboard_get_category_data_df_ss = dashboard_get_category_data_df
    
    # st.dataframe(st.session_state.dashboard_get_category_data_df_ss.style.format({"monthly": "${:,.2f}", "yearly": "${:,.2f}"}), hide_index=True, use_container_width=True)

    col1, col2, col3 = st.columns(3, border=True)
    with col1:
            st.write("Total Debit")
            debit_sum = st.session_state.dashboard_get_category_data_df_ss.loc[st.session_state.dashboard_get_category_data_df_ss['categorytype']=='Debit', 'monthly'].sum()
            st.write(f'$ {debit_sum:,.2f}')
    with col2:
        st.write("Total Credit")
        credit_sum = st.session_state.dashboard_get_category_data_df_ss.loc[st.session_state.dashboard_get_category_data_df_ss['categorytype']=='Credit', 'monthly'].sum()
        st.write(f'$ {credit_sum:,.2f}')
    with col3:
        st.write("Balance")
        balance = credit_sum - debit_sum
        st.write(f'$ {balance:,.2f}')
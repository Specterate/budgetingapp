import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection, execute_query
import datetime

# set page configuration and title
st.set_page_config(page_title="Dashboard", page_icon="📊", layout='wide', initial_sidebar_state='expanded')
st.title("Dashboard")

print('Application started -----------------------------------------------')
print('\n\n\n')

def refresh_dashboard():
    for key in st.session_state.keys():
        if key == 'user_email':
            pass
        else:
            del st.session_state[key]


def get_date_selection():
    st.session_state.start_date = st.session_state.date_selection[0]
    st.session_state.end_date = st.session_state.date_selection[1]
    try:
        # Query categories table from supabase
        st.session_state.dashboard_get_transaction_data_df_ss = pd.DataFrame.from_dict(st.session_state.conn.table("transactions").select("*").gte("date",st.session_state.start_date).lte("date",st.session_state.end_date).execute().data)
        # Convert get_data to pandas dataframe
        # dashboard_get_transaction_data_df = pd.DataFrame.from_dict(dashboard_get_transaction_data.data)
        # st.session_state.dashboard_get_transaction_data_df_ss = dashboard_get_transaction_data_df
        print(st.session_state.dashboard_get_transaction_data_df_ss)
    except Exception as e:
        st.error(f"Error fetching transaction data:")
        print(f'Error fetching transaction data: {e}')
        st.stop()

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
    

    # set session state for get data
    if 'dashboard_get_category_data_df_ss' not in st.session_state:

        # Query categories table from supabase
        dashboard_get_category_data = st.session_state.conn.table("categories").select("*").execute()

        # Convert get_data to pandas dataframe
        dashboard_get_category_data_df = pd.DataFrame.from_dict(dashboard_get_category_data.data)
        st.session_state.dashboard_get_category_data_df_ss = dashboard_get_category_data_df
    
    # st.dataframe(st.session_state.dashboard_get_category_data_df_ss.style.format({"monthly": "${:,.2f}", "yearly": "${:,.2f}"}), hide_index=True, use_container_width=True)

    debit_sum = st.session_state.dashboard_get_category_data_df_ss.loc[st.session_state.dashboard_get_category_data_df_ss['categorytype']=='Debit','monthly'].sum()
    if "debit_sum" not in st.session_state:
        st.session_state.debit_sum = debit_sum

    credit_sum = st.session_state.dashboard_get_category_data_df_ss.loc[st.session_state.dashboard_get_category_data_df_ss['categorytype']=='Credit','monthly'].sum()
    if "credit_sum" not in st.session_state:
        st.session_state.credit_sum = credit_sum

    balance = credit_sum - debit_sum
    if "balance" not in st.session_state:
        st.session_state.balance = balance

    col1, col2, col3 = st.columns(3, border=True)
    col1.metric(label="Total Debit", value=f'$ {st.session_state.debit_sum:,.2f}')
    col2.metric(label="Total Credit", value=f'$ {st.session_state.credit_sum:,.2f}')
    col3.metric(label="Balance", value=f'$ {st.session_state.balance:,.2f}')

    # Set the date range for the query
    today_date = datetime.date.today()

    st.session_state.date_selection = st.date_input(
        "Select the date range",
        value = [],
        format="YYYY-MM-DD",
        )
    


    submit_date = st.button("Get Data", type="primary", on_click=get_date_selection)
        
    if submit_date:
        
        # st.session_state.start_date = date_selection[0]
        # st.session_state.end_date = date_selection[1]

        # # set session state for get trasaction data
        # try:
        #     if 'dashboard_get_transaction_data_df_ss' not in st.session_state:
        #         # Query categories table from supabase
        #         dashboard_get_transaction_data = st.session_state.conn.table("transactions").select("*").gte("date",st.session_state.start_date).lte("date",st.session_state.end_date).execute()
        #         # Convert get_data to pandas dataframe
        #         dashboard_get_transaction_data_df = pd.DataFrame.from_dict(dashboard_get_transaction_data.data)
        #         st.session_state.dashboard_get_transaction_data_df_ss = dashboard_get_transaction_data_df
        #         print(st.session_state.dashboard_get_transaction_data_df_ss)
        # except Exception as e:
        #     st.error(f"Error fetching transaction data:")
        #     print(f'Error fetching transaction data: {e}')
        #     st.stop()

        if st.session_state.dashboard_get_transaction_data_df_ss.empty:
            st.session_state.credit_sum = 0
            st.session_state.debit_sum = 0
            balance = 0
        else:
            st.session_state.credit_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("categorytype == 'Credit' and subcategory != 'Transfer'")['amount'].sum()
            print(f"Sum by credit: {credit_sum}")
            st.session_state.debit_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("categorytype == 'Debit' and subcategory != 'Transfer'")['amount'].sum()
            print(f"Sum by debit: {debit_sum}")
            st.session_state.balance = credit_sum - debit_sum
            print(f"Balance: {balance}")

        col1, col2 = st.columns(2, border=True)
        col1.metric(label="Total Debit", value=f'$ {st.session_state.debit_sum:,.2f}')
        col2.metric(label="Total Credit", value=f'$ {st.session_state.credit_sum:,.2f}')




    st.session_state
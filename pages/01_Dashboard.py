import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection, execute_query
import datetime
import plotly.express as px

# set page configuration and title
st.set_page_config(page_title="Dashboard", page_icon="📊", layout='wide', initial_sidebar_state='expanded')
st.title("Dashboard")

# Set spacing between application runs
print('\n\n\n')
print('Application started -----------------------------------------------')

# Function to refresh the keys in session_state
def refresh_dashboard():
    for key in st.session_state.keys():
        if key == 'user_email':
            pass
        else:
            del st.session_state[key]

# Function to retrieve the date selection from the user.
def get_date_selection():
    st.session_state.start_date = st.session_state.date_selection[0]
    st.session_state.end_date = st.session_state.date_selection[1]
    try:
        # Query transactions table from supabase and convert to dataframe
        st.session_state.dashboard_get_transaction_data_df_ss = pd.DataFrame.from_dict(st.session_state.conn.table("transactions").select("*").gte("date",st.session_state.start_date).lte("date",st.session_state.end_date).execute().data)
        print(st.session_state.dashboard_get_transaction_data_df_ss)
    except Exception as e:
        st.error(f"Error fetching transaction data:")
        print(f'Error fetching transaction data: {e}')
        st.stop()

# Set the sidebar
with st.sidebar:
    st.button("Refresh Page", type="primary", use_container_width=True, on_click=refresh_dashboard)

# Check if user is logged in
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
    
    tab1, tab2 = st.tabs(["Categories", "Transactions"])
    with tab1:

        # set session state for get category data
        if 'dashboard_get_category_data_df_ss' not in st.session_state:
            # Query categories table from supabase
            dashboard_get_category_data = st.session_state.conn.table("categories").select("*").execute()
            # Convert get_data to pandas dataframe
            st.session_state.dashboard_get_category_data_df_ss = pd.DataFrame.from_dict(dashboard_get_category_data.data)
        
        category_debit_sum = st.session_state.dashboard_get_category_data_df_ss.loc[st.session_state.dashboard_get_category_data_df_ss['categorytype']=='Debit','monthly'].sum()
        if "category_debit_sum" not in st.session_state:
            st.session_state.category_debit_sum = category_debit_sum

        category_credit_sum = st.session_state.dashboard_get_category_data_df_ss.loc[st.session_state.dashboard_get_category_data_df_ss['categorytype']=='Credit','monthly'].sum()
        if "category_credit_sum" not in st.session_state:
            st.session_state.category_credit_sum = category_credit_sum

        category_balance = category_credit_sum - category_debit_sum
        if "category_balance" not in st.session_state:
            st.session_state.category_balance = category_balance

        col1, col2, col3 = st.columns(3, border=True)
        col1.metric(label="Total Debit", value=f'$ {st.session_state.category_debit_sum:,.2f}')
        col2.metric(label="Total Credit", value=f'$ {st.session_state.category_credit_sum:,.2f}')
        col3.metric(label="Balance", value=f'$ {st.session_state.category_balance:,.2f}')

        px.bar(st.session_state.dashboard_get_category_data_df_ss, x='subcategory', y='monthly', color='categorytype', title="Monthly Budget by Category", color_discrete_sequence=px.colors.qualitative.Plotly).update_layout(showlegend=False).update_traces(texttemplate='%{value:,.2f}', textposition='outside').update_yaxes(title_text="Monthly Budget", title_standoff=25).update_xaxes(title_text="Subcategory", title_standoff=25).update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey'))).show()

    with tab2:
        # Set the date range for the query
        today_date = datetime.date.today()

        st.session_state.date_selection = st.date_input(
            "Select the date range",
            value = [],
            format="YYYY-MM-DD",
            )

        submit_date = st.button("Get Data", type="primary", on_click=get_date_selection)
            
        if submit_date:

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

with st.expander("See session state data"):
    st.session_state
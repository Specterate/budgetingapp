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
        st.switch_page("budgetingapp.py")
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
        
        
        category_debit_sum = st.session_state.dashboard_get_category_data_df_ss.query("categorytype == 'Debit' and category != 'Investment' and subcategory != 'Transfer'")['monthly'].sum()
        if "category_debit_sum" not in st.session_state:
            st.session_state.category_debit_sum = category_debit_sum

        category_credit_sum = st.session_state.dashboard_get_category_data_df_ss.query("categorytype == 'Credit' and category != 'Investment' and subcategory != 'Transfer'")['monthly'].sum()
        if "category_credit_sum" not in st.session_state:
            st.session_state.category_credit_sum = category_credit_sum

        category_investment_sum = st.session_state.dashboard_get_category_data_df_ss.query("categorytype == 'Investment'")['monthly'].sum()
        if "category_investment_sum" not in st.session_state:
            st.session_state.category_investment_sum = category_investment_sum

        category_balance = category_credit_sum - category_debit_sum - category_investment_sum
        if "category_balance" not in st.session_state:
            st.session_state.category_balance = category_balance

        # Display the metrics
        col1, col2, col3, col4 = st.columns(4, border=True)
        col1.metric(label="Total Debit", value=f'$ {st.session_state.category_debit_sum:,.2f}')
        col2.metric(label="Total Credit", value=f'$ {st.session_state.category_credit_sum:,.2f}')
        col3.metric(label="Total Investment", value=f'$ {st.session_state.category_investment_sum:,.2f}')
        col4.metric(label="Balance", value=f'$ {st.session_state.category_balance:,.2f}')

        with st.expander("Monthly Expenses by Category"):
            st.session_state.dashboard_category_debit = st.session_state.dashboard_get_category_data_df_ss.loc[st.session_state.dashboard_get_category_data_df_ss['categorytype']=='Debit']
            fig_debit = px.bar(
            st.session_state.dashboard_category_debit,
            x='category',
            y='monthly',
            color='categorytype',
            title='Monthly Expenses by Category',
            labels={'monthly': 'Monthly Expenses', 'category': 'category'},
            hover_data=['yearly'],
            text_auto='.2s'
        )
            fig_debit.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
            fig_debit.update_layout(
                xaxis_title="Category",
                yaxis_title="Monthly Expenses",
                title_x=0.5,
                title_y=0.95,
                title_font=dict(size=20),
                margin=dict(l=20, r=20, t=50, b=20),
                height=400,
            )
            st.plotly_chart(fig_debit, theme="streamlit")

        with st.expander("Monthly Expenses by Sub Category"):
            st.session_state.dashboard_category_debit = st.session_state.dashboard_get_category_data_df_ss.loc[st.session_state.dashboard_get_category_data_df_ss['categorytype']=='Debit']
            fig_debit = px.bar(
            st.session_state.dashboard_category_debit,
            x='subcategory',
            y='monthly',
            color='categorytype',
            title='Monthly Expenses by SubCategory',
            labels={'monthly': 'Monthly Expenses', 'Subcategory': 'Subcategory'},
            hover_data=['yearly'],
            text_auto='.2s'
        )
            fig_debit.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
            fig_debit.update_layout(
                xaxis_title="SubCategory",
                yaxis_title="Monthly Expenses",
                title_x=0.5,
                title_y=0.95,
                title_font=dict(size=20),
                margin=dict(l=20, r=20, t=50, b=20),
                height=400,
            )
            st.plotly_chart(fig_debit, theme="streamlit")            

        # Set session state for get category data           
            
        with st.expander("Monthly Income by Category"):
            st.session_state.dashboard_category_credit = st.session_state.dashboard_get_category_data_df_ss.query("categorytype == 'Credit' and category != 'Investment' and subcategory != 'Transfer'")
            fig = px.bar(
            st.session_state.dashboard_category_credit,
            x='monthly',
            y='subcategory',
            color='categorytype',
            title='Monthly Income by Subcategory',
            labels={'monthly': 'Monthly Expenses', 'subcategory': 'Subcategory'},
            hover_data=['yearly'],
            orientation='h',
            text_auto=True
        )
            st.plotly_chart(fig, theme="streamlit")


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
                st.session_state.transaction_credit_sum = 0
                st.session_state.transaction_debit_sum = 0
                st.session_state.transaction_investment_sum = 0
                st.session_state.transaction_balance = 0
            else:
                st.session_state.transaction_credit_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("categorytype == 'Credit' and subcategory != 'Transfer'")['amount'].sum()
                st.session_state.transaction_debit_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("categorytype == 'Debit' and subcategory != 'Investment' and subcategory != 'Transfer'")['amount'].sum()
                st.session_state.transaction_investment_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("subcategory == 'Investment'")['amount'].sum()
                st.session_state.transaction_balance = st.session_state.transaction_credit_sum - st.session_state.transaction_debit_sum - st.session_state.transaction_investment_sum

            col1, col2, col3, col4 = st.columns(4, border=True)
            col1.metric(label="Total Debit", value=f'$ {st.session_state.transaction_debit_sum:,.2f}')
            col2.metric(label="Total Credit", value=f'$ {st.session_state.transaction_credit_sum:,.2f}')
            col3.metric(label="Total Investment", value=f'$ {st.session_state.transaction_investment_sum:,.2f}')
            col4.metric(label="Balance", value=f'$ {st.session_state.transaction_balance:,.2f}')

    with st.expander("See session state data"):
        st.session_state
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
if "user_email" not in st.session_state or st.session_state.user_email is None:
    st.title("Dashboard - Welcome Guest")
else:
    st.title(f"Dashboard - Welcome {st.session_state.user_email}")

# Set spacing between application runs
print('\n\n\n')
print('Application started -----------------------------------------------')

# Function to refresh the dashboard
def refresh_dashboard():
    for key in st.session_state.keys():
        print(f'key is {key}')
        if key != 'user_email' and key != 'user_id' and key != 'conn':
            print(f"Deleting key: {key}")
            del st.session_state[key]

# Function to sign out
def sign_out():
    try:
        st.session_state.conn.auth.sign_out()
        for keys in st.session_state.keys():
            del st.session_state[keys]
    except Exception as e:
        st.error(f"Logout failed: {e}")


# Function to retrieve the date selection from the user.
def get_date_selection():
    st.session_state.start_date = st.session_state.date_selection[0]
    st.session_state.end_date = st.session_state.date_selection[1]
    try:
        # Query transactions table from supabase and convert to dataframe
        st.session_state.dashboard_get_transaction_data_df_ss = pd.DataFrame.from_dict(st.session_state.conn.table("transactions").select("*").eq("uuid", st.session_state.user_id).gte("date",st.session_state.start_date).lte("date",st.session_state.end_date).execute().data)
        print('st.session_state.dashboard_get_transaction_data_df_ss:')
        print(st.session_state.dashboard_get_transaction_data_df_ss)
    except Exception as e:
        st.error(f"Error fetching transaction data:")
        print(f'Error fetching transaction data: {e}')
        st.stop()

    try:        
        # set session state for get category data
        # Query categories table from supabase and convert to Pandas Dataframe
        dashboard_get_cate_trans_data = pd.DataFrame.from_dict(st.session_state.conn.table("categories").select("*").execute().data)
        st.session_state.dashboard_get_cate_trans_data_df_ss = dashboard_get_cate_trans_data
        print("st.session_state.dashboard_get_cate_trans_data_df_ss:")
        print(st.session_state.dashboard_get_cate_trans_data_df_ss)
    except Exception as e:
        st.error(f"Error fetching category data:")
        print(f'Error fetching category data: {e}')
        st.stop()

    try:
        merge_df = pd.merge(st.session_state.dashboard_get_transaction_data_df_ss, st.session_state.dashboard_get_cate_trans_data_df_ss, on=["subcategory"], how="left")
        print("\n merge_df:")
        print(merge_df)
    except Exception as e:
        st.error(f"Error merging data:")
        print(f'Error merging data: {e}')
        st.stop()

    try:
        st.session_state.dashboard_get_transaction_data_df_ss['category'] = merge_df['category']
        print("st.session_state.dashboard_get_transaction_data_df_ss:")
        print(st.session_state.dashboard_get_transaction_data_df_ss)
    except Exception as e:
        st.error(f"Error setting category data:")
        print(f'Error setting category data: {e}')
        st.stop()

# Set the sidebar for Refresh and Sign Out
with st.sidebar:
    st.button("Refresh Page", type="primary", use_container_width=True, on_click=refresh_dashboard)
    st.button('Sign Out', type="primary", use_container_width=True, on_click=sign_out)

# Check if user is logged in
if "user_email" not in st.session_state or st.session_state.user_email is None:
    st.write("User is not logged in")
    if st.button("Go to Login Page", type="primary"):
        # Redirect to login page
        st.switch_page("app_pages/00_Login.py")
else:
    # Set Supabase connection and session state
    if 'conn' not in st.session_state:
        conn = st.connection("supabase",type=SupabaseConnection)
        st.session_state.conn = conn
    
    tab1, tab2 = st.tabs(["Categories", "Transactions"])
    with tab1:

        # set session state for get category data
        if 'dashboard_get_category_data_df_ss' not in st.session_state:
            # Query categories table from supabase and convert to Pandas Dataframe
            dashboard_get_category_data = pd.DataFrame.from_dict(st.session_state.conn.table("categories").select("*").execute().data)
            st.session_state.dashboard_get_category_data_df_ss = dashboard_get_category_data

        # Sum up all the amounts in the Debit category
        category_debit_sum = st.session_state.dashboard_get_category_data_df_ss.query("categorytype == 'Debit' and category != 'Investment' and subcategory != 'Transfer'")['monthly'].sum()
        if "category_debit_sum" not in st.session_state:
            st.session_state.category_debit_sum = category_debit_sum

        # Sum up all the amounts in the Credit category
        category_credit_sum = st.session_state.dashboard_get_category_data_df_ss.query("categorytype == 'Credit' and category != 'Investment' and subcategory != 'Transfer'")['monthly'].sum()
        if "category_credit_sum" not in st.session_state:
            st.session_state.category_credit_sum = category_credit_sum

        # Sum up all the amounts in the Investment category
        category_investment_sum = st.session_state.dashboard_get_category_data_df_ss.query("categorytype == 'Investment'")['monthly'].sum()
        if "category_investment_sum" not in st.session_state:
            st.session_state.category_investment_sum = category_investment_sum

        # Calculate the balance aka monthly savings
        category_balance = category_credit_sum - category_debit_sum - category_investment_sum
        if "category_balance" not in st.session_state:
            st.session_state.category_balance = category_balance

        # Display the metrics from the categories
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

    # Section for checking Transaction data.
    with tab2:
        # Set the date range for the query
        today_date = datetime.date.today()

        # Store the input of the data selection
        st.session_state.date_selection = st.date_input(
            "Select the date range",
            value = [],
            format="YYYY-MM-DD",
            )

        # Query based on individual category
        # Get the list of categories and add it to a list        
        st.session_state.individual_category = st.session_state.dashboard_get_category_data_df_ss['category'].unique().tolist()
        # Sort the list of categories by alpha
        st.session_state.individual_category.sort()
        # Add the "All" category option to return all results
        st.session_state.individual_category.insert(0, 'All')
        print("st.session_state.individual_category:")
        print(st.session_state.individual_category)

        # Display a select box with options of categories
        st.session_state.selected_category = st.selectbox("Select Category", st.session_state.individual_category)
        print(f'Selected Category is {st.session_state.selected_category}')

        if st.session_state.date_selection:
            # Button to submit the date selection and query the data for the time frame
            submit_date = st.button("Get Data", type="primary", on_click=get_date_selection)

            # Check if the button was clicked
            if submit_date:
                print(f'what is the selected_category: {st.session_state.selected_category}')
                # Check if no cateogry has been selected
                if st.session_state.selected_category == "All":
                    
                    # if no data return, set default values of $0
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

                        # Individual Categories
                        st.session_state.transaction_cate_food_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("category == 'Food'")['amount'].sum()
                        st.session_state.transaction_cate_car_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("category == 'Car'")['amount'].sum()
                        st.session_state.transaction_cate_council_rates_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("category == 'Council Rates'")['amount'].sum()
                        st.session_state.transaction_cate_fitness_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("category == 'Fitness'")['amount'].sum()
                        st.session_state.transaction_cate_electricity_gas_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("category == 'Electricity & Gas'")['amount'].sum()
                        st.session_state.transaction_cate_insurance_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("category == 'Insurance'")['amount'].sum()
                        st.session_state.transaction_cate_internet_phone_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("category == 'Internet & Phone'")['amount'].sum()
                        st.session_state.transaction_cate_misc_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("category == 'Misc'")['amount'].sum()  
                        st.session_state.transaction_cate_mortgage_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("category == 'Mortgage'")['amount'].sum()
                        st.session_state.transaction_cate_pet_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("category == 'Pet'")['amount'].sum()
                        st.session_state.transaction_cate_rent_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("category == 'Rental Income'")['amount'].sum()
                        st.session_state.transaction_cate_salary_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("category == 'Salary'")['amount'].sum()
                        st.session_state.transaction_cate_strata_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("category == 'Strata'")['amount'].sum()
                        st.session_state.transaction_cate_subscriptions_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("category == 'Subscriptions'")['amount'].sum()
                        st.session_state.transaction_cate_sydney_water_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("category == 'Sydney Water'")['amount'].sum()
                        st.session_state.transaction_cate_transfer_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("category == 'Transfer'")['amount'].sum()
                        st.session_state.transaction_cate_transport_sum = st.session_state.dashboard_get_transaction_data_df_ss.query("category == 'Transport'")['amount'].sum()


                    st.write('Total Summary')

                    col1, col2, col3, col4 = st.columns(4, border=True)
                    col1.metric(label="Total Debit", value=f'$ {st.session_state.transaction_debit_sum:,.2f}')
                    col2.metric(label="Total Credit", value=f'$ {st.session_state.transaction_credit_sum:,.2f}')
                    col3.metric(label="Total Investment", value=f'$ {st.session_state.transaction_investment_sum:,.2f}')
                    col4.metric(label="Balance", value=f'$ {st.session_state.transaction_balance:,.2f}')

                    st.write('Individual Categories - Spending')

                    with st.container(border=True):
                        col5, col6, col7, col8 = st.columns(4, border=True)
                        col5.metric(label="Food", value=f'$ {st.session_state.transaction_cate_food_sum:,.2f}')
                        col6.metric(label="Car", value=f'$ {st.session_state.transaction_cate_car_sum:,.2f}')
                        col7.metric(label="Council Rates", value=f'$ {st.session_state.transaction_cate_council_rates_sum:,.2f}')
                        col8.metric(label="Electricity & Gas", value=f'$ {st.session_state.transaction_cate_electricity_gas_sum:,.2f}') 

                        col9, col10, col11, col12 = st.columns(4, border=True)
                        col9.metric(label="Fitness", value=f'$ {st.session_state.transaction_cate_fitness_sum:,.2f}')
                        col10.metric(label="Insurance", value=f'$ {st.session_state.transaction_cate_insurance_sum:,.2f}')
                        col11.metric(label="Internet & Phone", value=f'$ {st.session_state.transaction_cate_internet_phone_sum:,.2f}')
                        col12.metric(label="Misc", value=f'$ {st.session_state.transaction_cate_misc_sum:,.2f}')

                        col13, col14, col15, col16 = st.columns(4, border=True) 
                        col13.metric(label="Mortgage", value=f'$ {st.session_state.transaction_cate_mortgage_sum:,.2f}')
                        col14.metric(label="Pet", value=f'$ {st.session_state.transaction_cate_pet_sum:,.2f}')
                        col15.metric(label="Strata", value=f'$ {st.session_state.transaction_cate_strata_sum:,.2f}')
                        col16.metric(label="Subscriptions", value=f'$ {st.session_state.transaction_cate_subscriptions_sum:,.2f}')

                        col17, col18, col19, col20 = st.columns(4, border=True)
                        col17.metric(label="Sydney Water", value=f'$ {st.session_state.transaction_cate_sydney_water_sum:,.2f}')
                        col18.metric(label="Transport", value=f'$ {st.session_state.transaction_cate_transport_sum:,.2f}')
                        
                    st.write('Individual Categories - Income')
                    with st.container(border=True):
                        col1, col2 = st.columns(2, border=True)
                        col1.metric(label="Rental Income", value=f'$ {st.session_state.transaction_cate_rent_sum:,.2f}')
                        col2.metric(label="Salary", value=f'$ {st.session_state.transaction_cate_salary_sum:,.2f}')

                # Else if a category has been selected
                else:
                    st.write("Category selected")
                    print(st.session_state.dashboard_get_transaction_data_df_ss)
                    category_selected_df = st.session_state.dashboard_get_transaction_data_df_ss.loc[(st.session_state.dashboard_get_transaction_data_df_ss["category"] == st.session_state.selected_category)]
                    print(category_selected_df)

                    # Calculate the length of the data frame and multiple by 36 for pixels of the data_editor cell
                    length = len(category_selected_df)
                    print(f'length of file_import_df is {length}')
                    if length < 50:
                        data_editor_height_display = (length + 1 ) * 36
                    else:
                        data_editor_height_display = 50 * 36

                    st.data_editor(
                        category_selected_df,
                        hide_index = True,
                        height = data_editor_height_display,
                        column_order=("date", "description", "subcategory", "amount"),
                        column_config={
                            "subcategory": st.column_config.TextColumn(
                            "Subcategories",
                            width="medium",
                            ),
                            "description": st.column_config.TextColumn(
                            "Description",
                            width="medium",
                            ),
                            "amount": st.column_config.NumberColumn(
                            "Amount",
                            width="small",
                            format="dollar",
                            ),
                },
                        )

    # Check if admin user is logged in
    if "user_id" not in st.session_state:
        pass
    elif st.session_state.user_id == '3ea984ac-111b-4aca-8595-2c112f4918b5':
        with st.expander("Session State", expanded=False):
            st.session_state
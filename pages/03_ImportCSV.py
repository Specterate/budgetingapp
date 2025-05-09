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

st.set_page_config(page_title='Import/Export', layout='wide', initial_sidebar_state='expanded')
st.title('Import/Export Files')

print('Application started -----------------------------------------------')
# Function to load CSS from the 'assets' folder
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load the external CSS
css_path = pathlib.Path('style.css')
load_css(css_path)

def refresh_dashboard():
    for key in st.session_state.keys():
        if key == 'user_email':
            pass
        else:
            del st.session_state[key]

def data_editor_callback_for_final_result_df():
    if st.session_state['data_editor_changes']['edited_rows']:
        for index, changes in st.session_state['data_editor_changes']['edited_rows'].items():
            for col, value in changes.items():
                st.session_state.final_result_df.loc[index, col] = value
          
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

    bank_type = st.selectbox("Select Bank Account", ['Amex', 'ANZ', 'Westpac'],)
    
    uploaded_file = st.file_uploader("Please ensure the file is in CSV format and contains the required columns as Date, Description, Amount", label_visibility ="visible", help="Upload a CSV file with the required columns")
    if uploaded_file is not None:
        try:
            file_import_df = pd.read_csv(uploaded_file, usecols=['Date', 'Description', 'Amount'])
        except ValueError as e:
            print(f"Error reading file: {e}")
            st.error("Error reading file, please ensure the following columns are present - Date, Description, Amount")
            st.stop()

        # Get the lowest date from the file
        file_import_df.columns = file_import_df.columns.str.lower()
        file_import_df['date'] = pd.to_datetime(file_import_df['date'], dayfirst=True).dt.strftime('%Y-%m-%d')
        if bank_type == 'Amex':
            file_import_df["accounttype"] = "Amex"
            file_import_df['categorytype'] = np.where(file_import_df['amount'] < 0, 'Credit', 'Debit')
        elif bank_type == 'ANZ':
            file_import_df["accounttype"] = "ANZ"
            file_import_df['categorytype'] = np.where(file_import_df['amount'] < 0, 'Credit', 'Debit')
        elif bank_type == 'Westpac':
            file_import_df["accounttype"] = "Westpac"
            file_import_df['categorytype'] = np.where(file_import_df['amount'] < 0, 'Credit', 'Debit')
        file_import_df["subcategory"] = "Uncategorized"
        
        minimum_date = file_import_df['date'].min()
        maximum_date = file_import_df['date'].max()
        print(file_import_df)

        # Query Data from Category Table
        get_data_from_categories = st.session_state.conn.table("categories").select("subcategory").execute()
        get_data_from_categories_df = pd.DataFrame.from_dict(get_data_from_categories.data)
        key = 'subcategory'
        list_of_subcategories = [d.get(key) for d in get_data_from_categories.data if key in d]
        list_of_subcategories.sort()

        # Query Data from Transaction Table
        get_data_from_transactions = st.session_state.conn.table("transactions").select("*").gte("date", minimum_date).execute()
        if get_data_from_transactions.data == []:
            get_data_from_transactions_df_no_index = pd.DataFrame(columns=['date', 'accounttype', 'description', 'categorytype', 'subcategory', 'amount'])
        else:
            get_data_from_transactions_df = pd.DataFrame.from_dict(get_data_from_transactions.data)
            # drop index column for get_data_from_transactions_df
            get_data_from_transactions_df_no_index = get_data_from_transactions_df.drop(columns=['id'])

        # Query data from category_assignment
        get_data_from_category_assignment = st.session_state.conn.table('category_assignment').select("*").execute()
        if get_data_from_category_assignment == []:
            get_data_from_category_assignment_df = pd.DataFrame(columns=['description', 'subcategory'])
        else:
            get_data_from_category_assignment_df = pd.DataFrame.from_dict(get_data_from_category_assignment.data)

        if "get_data_from_category_assignment_df" not in st.session_state:
            st.session_state.get_data_from_category_assignment_df = get_data_from_category_assignment_df
            
        # Check if the dataframe from the database is empty and then
        # merge dataframe from import and dataframe from database
        if get_data_from_transactions_df_no_index.empty:
            full_df = file_import_df
        else:
            full_df = pd.concat([get_data_from_transactions_df_no_index, file_import_df], ignore_index=True)

        print('full_df')     
        print(full_df)

        # drop duplicates from the full_df
        full_df_drop_duplicates = full_df.drop_duplicates()

        print('full_df_drop_duplicates')
        print(full_df_drop_duplicates)

        # Merge the existing data from the database with the imported file (after dropping duplicates)
        merged_df = pd.merge(get_data_from_transactions_df_no_index, full_df_drop_duplicates, on=['date', 'accounttype', 'description', 'categorytype', 'subcategory', 'amount'], how='right', indicator=True)
        # Only return the rows in the dataframe that are not in the database
        final_result_df = merged_df[merged_df['_merge'] == 'right_only'].drop(columns=['_merge'])

        if "final_result_df" not in st.session_state:
            st.session_state.final_result_df = final_result_df

        print('final_result_df')
        print(final_result_df)

        # for index, row in st.session_state.final_result_df.iterrows():
        #     # Check if the description is already in the category_assignment table
        #     if row['description'] in st.session_state.get_data_from_category_assignment_df['description'].values:
        #         # Get the corresponding subcategory from the category_assignment table
        #         subcategory = st.session_state.get_data_from_category_assignment_df.loc[st.session_state.get_data_from_category_assignment_df['description'] == row['description'], 'subcategory'].values[0]
        #         st.session_state.final_result_df.at[index, 'subcategory'] = subcategory
        #     else:
        #         # If not found, set the subcategory to "Uncategorized"
        #         st.session_state.final_result_df.at[index, 'subcategory'] = "Uncategorized"

        st.subheader('Review data before importing')

        # display the data in a dataeditor so that we can update the subcategory
        "Un-Categorized"
        st.data_editor(
            st.session_state.final_result_df,
            num_rows="dynamic",
            key="data_editor_changes",
            on_change=data_editor_callback_for_final_result_df,
            hide_index = True,
            use_container_width=True,
            column_config={
                "subcategory": st.column_config.SelectboxColumn(
                "Subcategories",
                help="Select or add a subcategory",
                width="medium",
                options=list_of_subcategories,
                required=True,
                ),
                "categorytype": st.column_config.SelectboxColumn(
                "Category Type",
                help="Select or add a category type",
                width="medium",
                options=["Debit","Credit","NA"],
                required=True,
                ),
                "description": st.column_config.TextColumn(
                "Description",
                help="Enter a description",
                width="medium",
                ),
                "amount": st.column_config.NumberColumn(
                "Amount",
                help="Enter an amount",
                width="small",
                format="dollar",
                ),
            },
        )

        # To check if the final dataframe is empty to avoid sending random empty data to database
        if st.session_state.final_result_df.empty:
            st.html("<p><span style='color:red; font-size:30px'>No data to import!</span></p>")
            button_disabled = True
        elif (st.session_state.final_result_df['subcategory'] =="").any:
            st.html("<p><span style='color:red; font-size:30px'>Missing categories</span></p>")
            button_disabled = True
        else:
            button_disabled = False

        add_df_data = st.button('Import', type="primary", use_container_width=True, disabled=button_disabled)
        if add_df_data:
            try:
                # Add DataFrame to the database
                st.session_state.conn.table("transactions").insert(st.session_state.uncategorized_df.to_dict(orient='records')).execute()
                st.success('Added to Database!')     
            except Exception as e:
                st.write(e)


st.button("Refresh", type="secondary", use_container_width=True, on_click=refresh_dashboard)

st.session_state
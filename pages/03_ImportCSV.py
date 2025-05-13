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

st.set_page_config(page_title='Import/Export', layout='wide', initial_sidebar_state='expanded')
st.title('Import/Export Files')

print('Application started -----------------------------------------------')

# Function to load CSS from the 'assets' folder
def load_css(file_path):
    with open(file_path) as css_file:
        css_content = css_file.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# Load the external CSS
css_path = pathlib.Path('style.css')
load_css(css_path)

# Function to refresh the dashboard
def refresh_dashboard():
    for key in st.session_state.keys():
        if key != 'user_email':
            del st.session_state[key]

# Function to handle data editor changes
def data_editor_callback_for_final_result_df():
    if st.session_state['data_editor_changes']['edited_rows']:
        for index, changes in st.session_state['data_editor_changes']['edited_rows'].items():
            for col, value in changes.items():
                st.session_state.final_result_df.loc[index, col] = value

def clear_file_upload_state():
    if 'uploaded_file' in st.session_state:
        del st.session_state['uploaded_file']
        del st.session_state['final_result_df']

def clear_open_ai_run():
    if 'open_ai_run' in st.session_state:
        del st.session_state['open_ai_run']

def openai_classification(desc, str_list_of_subcategories):

    content_system = ("I would like to classify my expenses using specific categories. In input you will have the list of categories and the description of an expense. Please associate a category to the expense. "
    "Please only respond with the exact name of the category listed and nothing else. " + "Categories: \n") + str_list_of_subcategories

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": content_system},
            {"role": "user", "content": "Expense description: " + str(desc)}]
)      
    data = completion.choices[0].message
    print(f'data is {data.content}')
    return data.content

# Sidebar
with st.sidebar:
    st.button("Refresh Page", type="primary", use_container_width=True, on_click=refresh_dashboard)

# Get the OpenAI key from secrets
try:
    open_ai_key_value = st.secrets["openai_key"]["openai_secret_key"]
    client = OpenAI(api_key=open_ai_key_value)
except KeyError:
    st.error("OpenAI key not found in secrets. Please set it up in the Streamlit secrets manager.")
    st.stop()

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

    # Select Bank Statements (CSV) for different formatting.
    bank_type = st.selectbox("Select Bank Account", ['Amex', 'ANZ', 'Westpac'],)
    
    # Upload CSV file
    uploaded_file = st.file_uploader("Please ensure the file is in CSV format and contains the required columns as Date, Description, Amount", label_visibility ="visible", help="Upload a CSV file with the required columns", key='uploaded_file')
    if uploaded_file is not None:
        try:
            file_import_df = pd.read_csv(uploaded_file, usecols=['Date', 'Description', 'Amount'])
        except ValueError as e:
            print(f"Error reading file: {e}")
            st.error("Error reading file, please ensure the following columns are present - Date, Description, Amount")
            st.stop()

        # Set the column names to lower case
        file_import_df.columns = file_import_df.columns.str.lower()

        try:
            # Assign values to the columns
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
        except Exception as e:
            print(f"Error processing file: {e}")
            st.error("Error processing file, please ensure the following columns are present - Date, Description, Amount")
            st.stop()
        
        # Get the lowest date from the file
        minimum_date = file_import_df['date'].min()
        maximum_date = file_import_df['date'].max()
        print(file_import_df)

        # Query Data from Category Table
        get_data_from_categories = st.session_state.conn.table("categories").select("subcategory").execute()
        get_data_from_categories_df = pd.DataFrame.from_dict(get_data_from_categories.data)
        key = 'subcategory'
        list_of_subcategories = [d.get(key) for d in get_data_from_categories.data if key in d]
        list_of_subcategories.sort()
        print('list_of_subcategories')
        print(list_of_subcategories.sort())
        str_list_of_subcategories = ','.join(list_of_subcategories)

        # Query Data from Transaction Table
        get_data_from_transactions = st.session_state.conn.table("transactions").select('date', 'accounttype', 'description', 'categorytype', 'amount').gte("date", minimum_date).execute()
        if get_data_from_transactions.data == []:
            get_data_from_transactions_df_no_index = pd.DataFrame(columns=['date', 'accounttype', 'description', 'categorytype', 'amount'])
        else:
            get_data_from_transactions_df_no_index = pd.DataFrame.from_dict(get_data_from_transactions.data)

        # Query data from category_assignment
        # get_data_from_category_assignment = st.session_state.conn.table('category_assignment').select("*").execute()
        # if get_data_from_category_assignment == []:
        #     get_data_from_category_assignment_df = pd.DataFrame(columns=['description', 'subcategory'])
        # else:
        #     get_data_from_category_assignment_df = pd.DataFrame.from_dict(get_data_from_category_assignment.data)

        # if "get_data_from_category_assignment_df" not in st.session_state:
        #     st.session_state.get_data_from_category_assignment_df = get_data_from_category_assignment_df
            
        # Check if the dataframe from the database is empty and then
        # merge dataframe from import and dataframe from database
        if get_data_from_transactions_df_no_index.empty:
            full_df = file_import_df
        else:
            full_df = pd.concat([get_data_from_transactions_df_no_index, file_import_df], ignore_index=True)

        print('full_df')     
        print(full_df)

        # full_df = full_df.drop(columns=['subcategory'])
        print('printing full_df after dropping subcategory')
        print(full_df)

        # drop duplicates from the full_df
        full_df_drop_duplicates = full_df.drop_duplicates()
        print('full_df_drop_duplicates')
        print(full_df_drop_duplicates)

        # Merge the existing data from the database with the imported file (after dropping duplicates)
        merged_df = pd.merge(get_data_from_transactions_df_no_index, full_df_drop_duplicates, on=['date', 'accounttype', 'description', 'categorytype', 'amount'], how='right', indicator=True)

        # Only return the rows in the dataframe that are not in the database
        final_result_df = merged_df[merged_df['_merge'] == 'right_only'].drop(columns=['_merge'])
        final_result_df.reset_index(drop=True, inplace=True)
        final_result_df['subcategory'] = "Uncategorized"

        if "final_result_df" not in st.session_state:
            st.session_state.final_result_df = final_result_df

        print('final_result_df')
        print(final_result_df)


        length = len(file_import_df)
        progress_time = int(100 / length)
        new_progress_time = 0
        progress_bar = st.progress(0)

        if "open_ai_run" not in st.session_state:
            # Using OpenAI to classify the description and add the subcategories
            for index, row in final_result_df.iterrows():
                subcategory = openai_classification(row['description'], str_list_of_subcategories)
                final_result_df.at[index, 'subcategory'] = subcategory
                if index == length - 1:
                    st.success("Loading complete!")
                    progress_bar.progress(100)
                    break
                else:
                    progress_bar.progress(new_progress_time + progress_time)
                    new_progress_time += progress_time
                time.sleep(0.5)
            st.session_state.open_ai_run = True


        st.subheader('Review data before importing')

        if st.session_state.final_result_df.empty:
            st.warning("No new data to import")
            st.stop()
        else:
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

        add_df_data = st.button('Import', type="primary", use_container_width=True)
        if add_df_data:
            try:
                # Add DataFrame to the database
                response = st.session_state.conn.table("transactions").insert(st.session_state.final_result_df.to_dict(orient='records')).execute()
                print(f"Response from Supabase: {response}")
                with st.spinner("Uploading to Supabase", show_time=True):
                    time.sleep(5)
                st.success('Added to Database!')
                clear_file_upload_state()
                clear_open_ai_run()
                st.rerun()
            except Exception as e:
                e_exception = type(e).__name__
                print(f"Error adding data to database: {e}")
                if e_exception == 'APIError':
                    st.error("Error adding data to database, please check the logs for more details")
                else:
                    st.error("Re-check logs for exception")
                st.stop()

print(st.session_state)
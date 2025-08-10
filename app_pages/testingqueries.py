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

st.set_page_config(page_title='Import/Export', layout='wide', initial_sidebar_state='expanded')
if "user_email" not in st.session_state or st.session_state.user_email is None:
    st.title("Import/Export - Welcome Guest")
else:
    st.title(f"Import/Export - Welcome {st.session_state.user_email}")

print('\n\n\n')
print(f'Application started {datetime.datetime.now()} -----------------------------------------------')

# Function to refresh the dashboard
def refresh_dashboard():
    for key in st.session_state.keys():
        print(f'key is {key}')
        if key != 'user_email' and key != 'user_id' and key != 'conn':
            print(f"Deleting key: {key}")
            del st.session_state[key]   
def sign_out():
    try:
        st.session_state.conn.auth.sign_out()
        for keys in st.session_state.keys():
            del st.session_state[keys]
    except Exception as e:
        st.error(f"Logout failed: {e}")
        refresh_dashboard()
def clear_open_ai_run():
    if 'open_ai_run' in st.session_state:
        del st.session_state['open_ai_run']

def openai_classification(desc, str_list_of_subcategories):

    content_system = ("I would like to classify my expenses using specific categories. In input you will have the list of categories and the description of an expense. Please associate a category to the expense. Try to identify key words in the description that would help you to classify the expense into a specific category. For example moomoo is for investment" +
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
    st.button("Sign Out", type="primary", use_container_width=True, on_click=sign_out)

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
        st.switch_page("app_pages/00_Login.py")
else:
    # Set Supabase connection and session state
    if 'conn' not in st.session_state:
        conn = st.connection("supabase",type=SupabaseConnection)
        st.session_state.conn = conn

    # get description, subcategory from transactions from supabase based on uuid
    if 'full_transactions_df' not in st.session_state:
        st.session_state.full_transactions_df = pd.DataFrame.from_dict(st.session_state.conn.table("transactions").select("description, subcategory").eq("uuid", st.session_state.user_id).execute().data)

    st.write(st.session_state.full_transactions_df)
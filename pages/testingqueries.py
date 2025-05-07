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

def refresh_data_1_table():
    if st.session_state['data_1']['edited_rows']:
        for index, changes in st.session_state['data_1']['edited_rows'].items():
            print(f'index is {index}')
            print(f'changes is {changes}')
            for col, value in changes.items():
                st.session_state.data_1.loc[index, col] = value    

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

    data_1 = {'id': [1, 2, 3],'name': ['John', 'Jane', 'Doe'],'age': [28, 34, 45]}
    data_1_df = pd.DataFrame.from_dict(data_1)

    if "data_1" not in st.session_state:
        st.session_state['data_1'] = data_1_df

    st.data_editor(
        data_1,
        key=st.session_state['data_1'],
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic"
        )

st.session_state['data_1']

st.button("Refresh Dashboard", on_click=refresh_dashboard, type="primary")
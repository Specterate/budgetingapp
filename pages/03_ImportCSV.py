import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection, execute_query

st.set_page_config(page_title='Import/Export')
st.title('Expenses')

# set page configuration and title
st.set_page_config(page_title="Dashboard", page_icon="📊")
st.title("Dashboard")

def refresh_dashboard():
    for key in st.session_state.keys():
        if key == 'user_email':
            pass
        else:
            del st.session_state[key]

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

      uploaded_file = st.file_uploader("Choose a file")
      if uploaded_file is not None:
         dataframe = pd.read_csv(uploaded_file)
         st.data_editor(dataframe)

      add_df_data = st.button('Add DataFrame to Database')
      if add_df_data:
         # Add DataFrame to the database
         conn.table("mytable1").insert(dataframe.to_dict(orient='records')).execute()
         st.success('DataFrame added to the database!')     



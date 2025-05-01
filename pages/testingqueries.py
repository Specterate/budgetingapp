import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection, execute_query


# set page configuration and title
st.set_page_config(page_title="TestingQueries")
st.title("Testing Queries")

if "user_email" not in st.session_state or st.session_state.user_email is None:
    st.write("User is not logged in")
    if st.button("Go to Login Page", type="primary"):
        # Redirect to login page
        st.switch_page("Budgettingapp.py")
else:
    st.write("User is logged in")
    if "conn" not in st.session_state:
        conn = st.connection("supabase",type=SupabaseConnection)
        st.session_state.conn = conn

    categories_data_df = pd.DataFrame.from_dict(st.session_state.conn.table("mytable1").select("*").execute().data)
    st.session_state.categories_data_df = categories_data_df

    st.write("Categories Data")
    st.write(st.session_state.categories_data_df)
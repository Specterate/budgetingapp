import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection, execute_query

# set page configuration and title
st.set_page_config(page_title="Dashboard", page_icon="📊")
st.title("Dashboard")

if st.session_state.user_email is None:
    st.write("User is not logged in")
    if st.button("Go to Login Page", type="primary"):
        # Redirect to login page
        st.switch_page("Budgettingapp.py")
else:
    st.write("User is logged in")
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

# Function to refresh the dashboard
def refresh_dashboard():
    for key in st.session_state.keys():
        if key != 'user_email':
            del st.session_state[key]

# Sidebar
with st.sidebar:
    st.button("Refresh Page", type="primary", use_container_width=True, on_click=refresh_dashboard)

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


if st.session_state.user_id == '3ea984ac-111b-4aca-8595-2c112f4918b5':
    with st.expander("Session State", expanded=False):
        st.session_state
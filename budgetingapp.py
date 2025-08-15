import pandas as pd
import streamlit as st
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
# from st_supabase_connection import SupabaseConnection
from streamlit import session_state as ss
import pathlib
import gotrue

pages_no_auth = [
st.Page("app_pages/00_Login.py"),
st.Page("app_pages/01_Dashboard.py"), 
st.Page("app_pages/02_Categories.py"),
st.Page("app_pages/03_ImportCSV.py")]

pages_auth = [
st.Page("app_pages/00_Login.py"),
st.Page("app_pages/01_Dashboard.py"),  
st.Page("app_pages/02_Categories.py"),
st.Page("app_pages/03_ImportCSV.py"),
st.Page("app_pages/testingqueries.py"),
]

admin = '3ea984ac-111b-4aca-8595-2c112f4918b5'

# Check if admin user is logged in
if ("user_id" not in st.session_state or st.session_state.user_id != admin):
    pg = st.navigation(pages_no_auth)
elif st.session_state.user_id == admin:
    pg = st.navigation(pages_auth)
    

pg.run()


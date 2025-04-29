import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection

# set page configuration and title
st.set_page_config(page_title="Categories", page_icon="📚")
st.title("Categories")

if 'conn' not in st.session_state:
    conn = st.connection("supabase",type=SupabaseConnection)
    st.session_state.conn = conn

# Query categories table from supabase
rows = st.session_state.conn.table("categories").select("*").execute()

#display data
st.table(rows.data)
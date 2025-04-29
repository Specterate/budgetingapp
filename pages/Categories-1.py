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
get_data = st.session_state.conn.table("categories").select("*").execute()

# set session state for get data
if 'get_data' not in st.session_state:
    st.session_state.get_data = get_data

#display data
st.session_state.get_data

def update_data():
    pass

st.data_editor(st.session_state.get_data.data, use_container_width=True, hide_index=True, num_rows="dynamic", key="data_editor")
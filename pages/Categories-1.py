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

# Convert get_data to pandas dataframe

get_data_df = pd.DataFrame.from_dict(get_data.data)

# set session state for get data
if 'get_data_ss' not in st.session_state:
    st.session_state.get_data_ss = get_data_df

#display data
st.session_state.get_data_ss

def update_data():
    if st.session_state.data_editor['edited_rows']:
        for index, changes in st.session_state.data_editor['edited_rows'].items():
            for column, value in changes.items():
                st.session_state.get_data_ss.loc[index,column] = value

updates = st.data_editor(st.session_state.get_data.data, use_container_width=True, hide_index=True, num_rows="dynamic", key="data_editor", on_change=update_data)
import pandas as pd
import streamlit as st
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection

st.set_page_config(page_title="Categories", page_icon="📚")
st.title("Categories")

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

st.write('Categories Preview:')
rows = conn.table("categories").select("*").execute()
for row in rows.data:
    st.data_editor(row)

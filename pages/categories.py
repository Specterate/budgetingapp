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

def updated_categories():
    st.write("Updated Categories")

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

st.write('Categories Preview:')
rows = conn.table("categories").select("*").execute()
new_row = pd.DataFrame.from_dict(rows.data)
st.data_editor(
                new_row,
                column_order=['category', 'subcategory', 'monthly', 'yearly'],
                column_config={
                "monthly": st.column_config.NumberColumn(
                "Monthly",
                format="dollar"
            ),
                "yearly": st.column_config.NumberColumn(
                "Yearly",
                format="dollar"
            ),
            },
               hide_index=True,
               num_rows="dynamic",
               height=1000,
               on_change=updated_categories,)

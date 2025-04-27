import pandas as pd
import streamlit as st
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection
import st_aggrid as AgGrid

st.set_page_config(page_title="Categories", page_icon="📚")
st.title("Categories")

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

st.write('Categories Preview:')
rows = conn.table("categories").select("*").execute()
new_row = pd.DataFrame.from_dict(rows.data)
AgGrid(new_row)
# st.data_editor(
#                 new_row,
#                 column_order=['category', 'subcategory', 'monthly', 'yearly'],
#                 column_config={
#                 "monthly": st.column_config.NumberColumn(
#                 "Monthly",
#                 format="dollar"
#             ),
#                 "yearly": st.column_config.NumberColumn(
#                 "Yearly",
#                 format="dollar"
#             ),
#             },
#                hide_index=True,
#                num_rows="dynamic",
#                height=500,
#                )

with st.form(key='add_category_form'):
    category = st.text_input("Category")
    subcategory = st.text_input("Subcategory")
    monthly = st.number_input("Monthly", min_value=0)
    yearly = st.number_input("Yearly", min_value=0)
    submit_button = st.form_submit_button(label='Add Category')
    if submit_button:
        conn.table("categories").insert({"category": category, "subcategory": subcategory, "monthly": monthly, "yearly": yearly}).execute()
        st.success(f"Category {category} added successfully!")

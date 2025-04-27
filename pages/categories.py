import streamlit as st
import pandas as pd
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

def update_categories():
    conn.table("categories").upsert(st.session_state).execute()

st.write('Categories Preview:')
rows = conn.table("categories").select("*").execute()
# st.write(rows)
new_row = pd.DataFrame.from_dict(rows.data)

st.data_editor(
    rows.data,    
    column_config={
        "category": st.column_config.TextColumn("Category"),
        "subcategory": st.column_config.TextColumn("Subcategory"),
        "monthly": st.column_config.NumberColumn("Monthly", format="dollar"),
        "yearly": st.column_config.NumberColumn("Yearly", format="dollar"),
    },               
    hide_index=True,
    num_rows="dynamic",
    height=500,
    key="my_categories",
#    on_change=update_categories,
)
               
st.write("Here's the value in Session State:")
st.write(st.session_state["my_categories"])

# Using a Form to add a new category
# with st.form(key='add_category_form'):
#     category = st.text_input("Category")
#     subcategory = st.text_input("Subcategory")
#     monthly = st.number_input("Monthly", min_value=0)
#     yearly = st.number_input("Yearly", min_value=0)
#     submit_button = st.form_submit_button(label='Add Category')
#     if submit_button:
#         conn.table("categories").insert({"category": category, "subcategory": subcategory, "monthly": monthly, "yearly": yearly}).execute()
#         st.success(f"Category {category} added successfully!")

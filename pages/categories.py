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

# Initialize connection with Supabase
conn = st.connection("supabase",type=SupabaseConnection)

st.subheader('Categories Preview:', divider=True)

st.write('Getting data... ')
# Get all the categories from the Supabase
rows = conn.table("categories").select("*").execute()
st.write('Converting Data to Pandas DataFrame... ')
# Convert the data into a Pandas DataFrame
df = pd.DataFrame.from_dict(rows.data)

if "sd" not in st.session_state:
    st.session_state['sd'] = df

st.write("Session State is")
st.write(st.session_state['sd'])

def add_new_row(category, subcategory, monthly, yearly):
    st.session_state.new_added_row = pd.DataFrame.from_dict([{"category": category, "subcategory": subcategory, "monthly": monthly, "yearly": yearly}])
    df = pd.concat([df, st.session_state.new_added_row])
    del st.session_state['sd']
    st.session_state['sd'] = df
    conn.table("categories").insert({"category": category, "subcategory": subcategory, "monthly": monthly, "yearly": yearly}).execute()
    st.success(f"Category {category} added successfully!")

col1, col2 = st.columns(2)
with col1:
    # Using a Form to add a new category
    with st.form(key='add_category_form'):
        category = st.text_input("Category")
        subcategory = st.text_input("Subcategory")
        monthly = st.number_input("Monthly", min_value=0)
        yearly = st.number_input("Yearly", min_value=0)
        submit_button = st.form_submit_button(label='Add Category', on_click=add_new_row, args=(category,subcategory,monthly,yearly))        

            

with col2:
    # Delete Sub Category
    with st.form(key='delete_category_form'):
        delete_subcategory = st.selectbox("Select Sub Category to Delete", df['subcategory'].unique())
        delete_button = st.form_submit_button(label='Delete Sub Category')
        if delete_button:
            conn.table("categories").delete().eq("subcategory", delete_subcategory).execute()
            st.success(f"Category {delete_subcategory} deleted successfully!")

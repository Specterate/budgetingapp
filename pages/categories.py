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


def get_data():
    # Get all the categories from the Supabase
    rows = conn.table("categories").select("*").execute()

    # Convert the data into a Pandas DataFrame
    df = pd.DataFrame.from_dict(rows.data)

    st.write("writing DF")
    st.write(df)
    if "data" not in st.session_state:
        st.session_state.data = df
    # st.data_editor(
    #     df,    
    #     column_config=
    #     {
    #         "category": st.column_config.TextColumn("Category"),
    #         "subcategory": st.column_config.TextColumn("Subcategory"),
    #         "monthly": st.column_config.NumberColumn("Monthly", format="dollar"),
    #         "yearly": st.column_config.NumberColumn("Yearly", format="dollar"),
    #     },               
    #     hide_index=True,
    #     num_rows="dynamic",
    #     height=500,
    # )

    return df

new_row = get_data()
st.write(st.session_state.data)

col1, col2 = st.columns(2)
with col1:
    # Using a Form to add a new category
    with st.form(key='add_category_form'):
        category = st.text_input("Category")
        subcategory = st.text_input("Subcategory")
        monthly = st.number_input("Monthly", min_value=0)
        yearly = st.number_input("Yearly", min_value=0)
        submit_button = st.form_submit_button(label='Add Category', onclick=get_data)
        if submit_button:
            conn.table("categories").insert({"category": category, "subcategory": subcategory, "monthly": monthly, "yearly": yearly}).execute()
            st.success(f"Category {category} added successfully!")
            

with col2:
    # Delete Sub Category
    with st.form(key='delete_category_form'):
        delete_subcategory = st.selectbox("Select Sub Category to Delete", new_row['subcategory'].unique())
        delete_button = st.form_submit_button(label='Delete Sub Category', onclick=get_data)
        if delete_button:
            conn.table("categories").delete().eq("subcategory", delete_subcategory).execute()
            st.success(f"Category {delete_subcategory} deleted successfully!")

get_data()

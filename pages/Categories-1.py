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
"This is the session state data for get_data_ss"

# st.session_state.get_data_ss
st.session_state.get_data_ss

# Update data based on edits ['edited_rows'] in the data editor
def update_sub_category():
    # if st.session_state.data_editor['edited_rows']:
    #     for index, changes in st.session_state.data_editor['edited_rows'].items():
    #         for column, value in changes.items():
    #             st.session_state.get_data_ss.loc[index,column] = value
    pass

# Add new categories
def add_sub_category():
    new_row_df = pd.DataFrame.from_dict([{"category": st.session_state.category_name, "subcategory": st.session_state.sub_category_name, "monthly": st.session_state.monthly_expenses, "yearly": st.session_state.yearly_expenses}])
    st.session_state.get_data_ss = pd.concat([st.session_state.get_data_ss, new_row_df], ignore_index=True)
    
# Delete category
def delete_sub_category():
    st.session_state.get_data_ss = st.session_state.get_data_ss[st.session_state.get_data_ss.subcategory != st.session_state.sub_category_delete]

tab1, tab2, tab3 = st.tabs(["Add Category", "Delete Category", "Edit Exisitng Category"])
with tab1:
    with st.form("add_category", clear_on_submit=True, border=True):
            st.write("Add new Category")
            # st.session_state.name = st.text_input("Name", placeholder="Enter your name")
            # st.session_state.age = st.number_input("Age", min_value=0, max_value=100)
            # st.session_state.location = st.selectbox("Location", ["New York", "San Francisco", "Chicago", "Seattle"])
            category_name = st.text_input("Category Name", placeholder="Enter Category Name", key="category_name")
            sub_category_name = st.text_input("Sub Category Name", placeholder="Enter Sub Category Name (Unique)", key="sub_category_name")
            monthly_expenses = st.number_input("Monthly Expenses", key="monthly_expenses")
            yearly_expenses = st.number_input("Yearly Expenses", key="yearly_expenses")
            submitted = st.form_submit_button("Submit", type="secondary", on_click=add_sub_category)
with tab2:
    with st.form("delete_sub_category", clear_on_submit=True, border=True):
        st.write("Delete Sub Category")
        st.selectbox("Select Sub Category to delete", st.session_state.get_data_ss.subcategory.unique(), key="sub_category_delete")
        st.form_submit_button("Delete", type="primary", on_click=delete_sub_category)

with tab3:
    with st.form("edit_category", clear_on_submit=True, border=True):
        st.write("Edit Existing Category")
        sub_category_selection = st.selectbox("Select Sub Category to delete", st.session_state.get_data_ss.subcategory.unique(), key="sub_category_select", index=None)
        if sub_category_selection:
            st.session_state.edited_dataframe = st.session_state.get_data_ss[st.session_state.get_data_ss.subcategory.isin(sub_category_selection)]
            "Data Frame Edited is"
            st.write(st.session_state.edited_dataframe)
            category_name_update = st.text_input("Category Name", placeholder="Enter Category Name", key="category_name_update")
            monthly_expenses_update = st.number_input("Monthly Expenses", key="monthly_expenses_update")
            yearly_expenses_update = st.number_input("Yearly Expenses", key="yearly_expenses_update")
        st.form_submit_button("Update", type="secondary", on_click=update_sub_category)
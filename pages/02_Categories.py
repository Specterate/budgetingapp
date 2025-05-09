import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection, execute_query


# set page configuration and title
st.set_page_config(page_title="Categories", page_icon="📚", layout='wide', initial_sidebar_state='expanded')
st.title("Categories")

if "user_email" not in st.session_state or st.session_state.user_email is None:
    st.write("User is not logged in")
    if st.button("Go to Login Page", type="primary"):
        # Redirect to login page
        st.switch_page("Budgetingapp.py")
else:
    # Set Supabase connection and session state
    if 'conn' not in st.session_state:
        conn = st.connection("supabase",type=SupabaseConnection)
        st.session_state.conn = conn

    # set session state for get data
    if 'get_category_data_df_ss' not in st.session_state:

        # Query categories table from supabase
        get_category_data = st.session_state.conn.table("categories").select("*").execute()

        # Convert get_data to pandas dataframe
        get_category_data_df = pd.DataFrame.from_dict(get_category_data.data)
        st.session_state.get_category_data_df_ss = get_category_data_df

    st.subheader("Categories Data")
    st.dataframe(st.session_state.get_category_data_df_ss, hide_index=True, use_container_width=True)

    # Update data based on edits ['edited_rows'] in the data editor
    def update_sub_category():
        try:
            response = (st.session_state.conn.table("categories").update({"category": st.session_state.category_name_update, "monthly": st.session_state.monthly_expenses_update, "yearly": st.session_state.yearly_expenses_update, "categorytype": st.session_state.category_type_update}).eq("subcategory", st.session_state.sub_category_select).execute())
            index_value = st.session_state.edited_dataframe.index.item()
            st.session_state.get_category_data_df_ss.at[index_value, "category"] = st.session_state.category_name_update
            st.session_state.get_category_data_df_ss.at[index_value, "monthly"] = st.session_state.monthly_expenses_update
            st.session_state.get_category_data_df_ss.at[index_value, "yearly"] = st.session_state.yearly_expenses_update
            st.session_state.get_category_data_df_ss.at[index_value, "categorytype"] = st.session_state.category_type_update
        except Exception as e:
            st.error(f"Insert failed: {e}")

    # Add new categories
    def add_sub_category():
        if st.session_state.sub_category_name in st.session_state.get_category_data_df_ss.subcategory.unique(): 
            st.error("Sub Category already exists")
            return
        elif "category_name" not in st.session_state.category_name:
            st.error("Pleae enter Category Name")
            return
        else:
            try:
                response = (st.session_state.conn.table("categories").insert({"category": st.session_state.category_name, "subcategory": st.session_state.sub_category_name, "monthly": st.session_state.monthly_expenses, "yearly": st.session_state.yearly_expenses, "categorytype": st.session_state.category_type}).execute())
                new_row_df = pd.DataFrame.from_dict([{"category": st.session_state.category_name, "subcategory": st.session_state.sub_category_name, "monthly": st.session_state.monthly_expenses, "yearly": st.session_state.yearly_expenses, "categorytype": st.session_state.category_type}])
                st.session_state.get_category_data_df_ss = pd.concat([st.session_state.get_category_data_df_ss, new_row_df], ignore_index=True)
            except Exception as e:
                st.error(f"Insert failed: {e.message}")
        
    # Delete category
    def delete_sub_category():
        try:
            for deleted_subcategories in st.session_state.sub_category_delete:
                response = (st.session_state.conn.table("categories").delete().eq("subcategory", deleted_subcategories).execute())
            st.session_state.get_category_data_df_ss = st.session_state.get_category_data_df_ss[~st.session_state.get_category_data_df_ss.subcategory.isin(st.session_state.sub_category_delete)]
        except Exception as e:
            st.error(f"Delete failed: {e}")

    def edit_sub_category():
        edited_dataframe = st.session_state.get_category_data_df_ss[st.session_state.get_category_data_df_ss.subcategory.isin([st.session_state.sub_category_select])]
        st.session_state.edited_dataframe = edited_dataframe

    tab1, tab2, tab3 = st.tabs(["Add Category", "Delete Category", "Edit Exisitng Category"])
    with tab1:
        with st.form("add_category", clear_on_submit=True, border=True):
                st.write("Add new Category")
                category_name = st.text_input("Category Name", placeholder="Enter Category Name", key="category_name")
                sub_category_name = st.text_input("Sub Category Name", placeholder="Enter Sub Category Name (Unique)", key="sub_category_name")
                monthly_expenses = st.number_input("Monthly Expenses", key="monthly_expenses")
                yearly_expenses = st.number_input("Yearly Expenses", key="yearly_expenses")
                categorytype = st.selectbox("Category Type", ["Debit","Credit","NA"], key="category_type")
                submitted = st.form_submit_button("Submit", type="secondary", on_click=add_sub_category)
                

    with tab2:
        with st.form("delete_sub_category", clear_on_submit=True, border=True):
            st.multiselect("Select Sub Category to delete", st.session_state.get_category_data_df_ss.subcategory.unique(), key="sub_category_delete", max_selections=5)
            st.form_submit_button("Delete", type="primary", on_click=delete_sub_category)

    with tab3:
        st.write("Edit Existing Category")
        selectbox_selection = st.selectbox("Select Sub Category to edit", st.session_state.get_category_data_df_ss.subcategory.unique(), key="sub_category_select", on_change=edit_sub_category, index=None)
        if selectbox_selection is not None:
            st.write(st.session_state.edited_dataframe)
            with st.form("edit_category", clear_on_submit=True, border=True):
                category_name_update = st.text_input("Category Name", key="category_name_update", value=st.session_state.edited_dataframe['category'].values[0])
                monthly_expenses_update = st.number_input("Monthly Expenses", key="monthly_expenses_update", placeholder = st.session_state.edited_dataframe['monthly'].values[0], value=None, format="%.0f")
                yearly_expenses_update = st.number_input("Yearly Expenses", key="yearly_expenses_update", placeholder = st.session_state.edited_dataframe['yearly'].values[0], value=None, format="%.0f")
                categorytype_update = st.selectbox("Category Type", ["Debit","Credit","NA"], placeholder=None, key="category_type_update", accept_new_options=True)
                st.form_submit_button("Update", type="primary", on_click=update_sub_category)
                
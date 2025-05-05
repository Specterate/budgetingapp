import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection, execute_query
import datetime

#update

st.set_page_config(page_title='Import/Export')
st.title('Import/Export Files')

def refresh_dashboard():
    for key in st.session_state.keys():
        if key == 'user_email':
            pass
        else:
            del st.session_state[key]

if "user_email" not in st.session_state or st.session_state.user_email is None:
   st.write("User is not logged in")
   if st.button("Go to Login Page", type="primary"):
        # Redirect to login page
        st.switch_page("Budgettingapp.py")
else:
    # Set Supabase connection and session state
   if 'conn' not in st.session_state:
      conn = st.connection("supabase",type=SupabaseConnection)
      st.session_state.conn = conn

   # Upload the File
   uploaded_file = st.file_uploader("Choose a file")
   if uploaded_file is not None:
      file_import_df = pd.read_csv(uploaded_file)
      
      # Get the lowest date from the file
      file_import_df['date'] = pd.to_datetime(file_import_df['date'], dayfirst=True).dt.strftime('%Y-%m-%d')
      file_import_df = file_import_df.fillna(value="NA")
      minimum_date = file_import_df['date'].min()
      maximum_date = file_import_df['date'].max()
      
      # Get the minimum of the file_month
      # file_import_min_month = pd.Timestamp(minimum_date).month

      # Get the maximum of the file_month
      # file_import_max_month = pd.Timestamp(maximum_date).month

      # Query Data from Transaction Table
      get_data_from_transactions = st.session_state.conn.table("transactions").select("*").gte("date", minimum_date).execute()
      get_data_from_transactions_df = pd.DataFrame.from_dict(get_data_from_transactions.data)

      get_data_from_categories = st.session_state.conn.table("categories").select("subcategory").execute()
      get_data_from_categories_df = pd.DataFrame.from_dict(get_data_from_categories.data)
      st.write(get_data_from_categories.data)
      

      
      # drop index column for get_data_from_transactions_df
      get_data_from_transactions_df_no_index = get_data_from_transactions_df.drop(columns=['id'])

      # st.dataframe(get_data_from_transactions_df_no_index)

      full_df = pd.concat([get_data_from_transactions_df_no_index, file_import_df], ignore_index=True)
      # st.dataframe(full_df)

      full_df_drop_duplicates = full_df.drop_duplicates()

      # st.write('Updated')
      # st.dataframe(full_df_drop_duplicates)

      merged_df = pd.merge(get_data_from_transactions_df_no_index, full_df_drop_duplicates, on=['date', 'accounttype', 'description', 'categorytype', 'subcategory', 'amount'], how='right', indicator=True)
      # st.dataframe(merged_df)
      result_df = merged_df[merged_df['_merge'] == 'right_only'].drop(columns=['_merge'])
      st.data_editor(result_df,     column_config={
        "subcategory": st.column_config.SelectboxColumn(
            "App Category",
            help="The category of the app",
            width="medium",
            options=[],
            required=True,
        )
    },)

      add_df_data = st.button('Import')
      if add_df_data:
         try:
            # Add DataFrame to the database
            st.session_state.conn.table("transactions").insert(file_import_df.to_dict(orient='records')).execute()
            st.success('DataFrame added to the database!')     
         except Exception as e:
            st.write(e)



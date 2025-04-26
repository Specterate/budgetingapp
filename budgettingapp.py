import pandas as pd
import streamlit as st
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection

st.set_page_config(page_title='Budgetting App', page_icon=':moneybag:')
st.title('Budgetting App')

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

# Perform query.
rows = conn.table("mytable").select("*").execute()

capture_new_name = st.text_input("Enter person name", "enter name")
st.write(f'The name enteres is {capture_new_name}')
if st.button('Update Name'):
    response = (
        conn.table("mytable")
        .insert({"name": capture_new_name})
        .execute()
    )

# Print results.
for row in rows.data:
    st.write(f"{row['name']} has a :{row['pet']}:")

# # Creae a connection to Neon PostgreSQL database
# conn=st.connection("neon",type="sql")
# # Query the database
# df = conn.query("SELECT name, pet FROM home")
# df.reset_index(drop=True, inplace=True)
# st.data_editor(df)

# update_df = st.button('Update Data')
# if update_df:
#     with conn.session as session:
#         # Update the database with new data
#         session.execute(text("""
#                              INSERT INTO home 
#                              VALUES (?,?)), {'name': 'John', 'pet': 'Dog'}
#                              """))
#         session.commit()
#         st.success('Data updated successfully!')

# # with conn.session as session:
#     st.subheader('Upload your CSV file')
#     imported_file = st.file_uploader('', type='csv')
#     if imported_file is not None:
#         df = pd.read_csv(imported_file)
#         st.write('Data Preview:')
#         st.write(df)
#         df.to_sql('name', engine, if_exists='append', index=False)

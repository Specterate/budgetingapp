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

col1, col2 = st.columns(2, border=True)
with col1:
    # Add new name to the database
    capture_new_name = st.text_input("Enter person name", help="Enter name")
    st.write(f'The name entered is {capture_new_name}')
with col2:
    capture_new_pet = st.text_input("Enter pet name", help="Enter pet name")
    st.write(f'The pet entered is {capture_new_pet}')

with col1:
    if st.button('Add Name and Pet'):
        response = (
            conn.table("mytable")
            .insert({"name": capture_new_name, 
                    "pet": capture_new_pet})
            .execute()
        )

with col2:
    show_data = st.button('Show Data')
    if show_data:
        st.write('Data Preview:')
        # Perform query.
        rows = conn.table("mytable").select("*").execute()
        for row in rows.data:
            st.write(f"{row['name']}, {row['pet']}")



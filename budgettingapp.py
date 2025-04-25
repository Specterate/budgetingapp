import pandas as pd
import streamlit as st
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
import psycopg2
from sqlalchemy.engine import URL


st.set_page_config(page_title='Budgetting App', page_icon=':moneybag:')
st.title('Budgetting App')

# Creae a connection to Neon PostgreSQL database
conn=st.connection("neon",type="sql")

button_insert_query = st.button('Insert Query')
if button_insert_query:
    # Insert a row into the table
    with conn.session as session:
        df = session.execute(text("""
                                INSERT INTO home (name, pet) 
                                VALUES ('tyler', 'jack')
                                """))
    session.commit()
    st.write("Row inserted successfully!")     
        

# st.subheader('Upload your CSV file')
# imported_file = st.file_uploader('', type='csv')
# if imported_file is not None:
#     df = pd.read_csv(imported_file,index_col= 0)
#     st.write('Data Preview:')
#     st.write(df)
#     for row in df.itertuples():
#         name, pet = row[0], row[1]
#         # Insert the values into the database
#         with conn.session as session:
#             session.execute(text(f"INSERT home.values VALUES {name}, {pet};"))
#             session.commit()
# else:
#     st.write('Warning: Please upload a CSV file to get started.')


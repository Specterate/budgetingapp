import pandas as pd
import streamlit as st
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


st.set_page_config(page_title='Budgetting App', page_icon=':moneybag:')
st.title('Budgetting App')

# Creae a connection to Neon PostgreSQL database
conn=st.connection("neon",type="sql")
# Query the database
df = conn.query("SELECT name, pet FROM home")
df.reset_index(drop=True, inplace=True)
st.data_editor(df)


# with conn.session as session:
#     st.subheader('Upload your CSV file')
#     imported_file = st.file_uploader('', type='csv')
#     if imported_file is not None:
#         df = pd.read_csv(imported_file)
#         st.write('Data Preview:')
#         st.write(df)
#         df.to_sql('name', engine, if_exists='append', index=False)

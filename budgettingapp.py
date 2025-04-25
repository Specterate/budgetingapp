import pandas as pd
import streamlit as st
import numpy as np
import time
import os

st.set_page_config(page_title='Budgetting App', page_icon=':moneybag:')
st.title('Budgetting App')

# Creae a connection to Neon PostgreSQL database
conn=st.connection("neon",type="sql")
st.write(conn)

st.subheader('Upload your CSV file')
imported_file = st.file_uploader('', type='csv')
if imported_file is not None:
    df = pd.read_csv(imported_file,index_col= 0)
    st.write('Data Preview:')
    st.write(df)
    for row in df.itertuples():
        name, pet = row[0], row[1]
        # Insert the values into the database
        conn.execute("INSERT INTO home (name, pet) VALUES (%s, %s)", (name, pet))
else:
    st.write('Warning: Please upload a CSV file to get started.')


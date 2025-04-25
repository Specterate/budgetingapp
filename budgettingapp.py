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

button_insert_query = st.button('Insert Query', key='insert_query')
if button_insert_query:
    # Insert a row into the table
    with conn.session as session:
        df = session.execute(text("""
                                INSERT INTO home (name, pet) 
                                VALUES ('tyler', 'jack')
                                """))
        session.commit()
    st.write("Row inserted successfully!")     
        

st.subheader('Upload your CSV file')
imported_file = st.file_uploader('', type='csv')
if imported_file is not None:
    df = pd.read_csv(imported_file)
    st.write('Data Preview:')
    st.write(df)
    for row in df.itertuples():
        name, pet = row[1], row[2]
        st.write(f'Name: {name}, Pet: {pet}')
    # st.write('Data Preview:')
    # Insert the values into the database
    # with conn.session as session:
    #     session.execute('home', df, if_exists='append', index=False)
    #     # session.execute(text("""
    #     #                      INSERT INTO home (id, name, pet)
    #     #                      VALUES (NULL, {name},{pet})
    #     #                      """.format(name=name, pet=pet)))
    #     session.commit()
else:
    st.write('Warning: Please upload a CSV file to get started.')


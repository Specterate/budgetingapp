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
    for row in df.iterrows():
        name, pet = str(f'{row[0]}'), str(f'{row[1]}')
        st.write(f'Name: {name}, Pet: {pet}')
    # Insert the values into the database
        with conn.session as session:
            new_data = (name, pet)
            st.write(f'The new data is {new_data}')
            st.write(f'Waiting for 5 seconds....') 
            time.sleep(5)
            # Define the SQL query to insert the data
            query = text("""
            INSERT INTO home ("name", "pet") 
            VALUES (:name, :pet)
            """)
            session.execute(text(query), {'name': name, 'pet': pet})
            # Commit the transaction
            session.commit()
            st.write("Row inserted successfully!")
else:
    st.write('Warning: Please upload a CSV file to get started.')

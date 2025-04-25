import pandas as pd
import streamlit as st
import numpy as np
import time
import os

st.set_page_config(page_title='Budgetting App', page_icon=':moneybag:')
st.title('Budgetting App')

# Creae a connection to Neon PostgreSQL database
conn=st.connection("neon",type="sql")

st.write(st.session_state)

def update_session_state_for_buttons():
    if st.session_state.show_data_from_neon1 == False:
        st.write("Else Option Selected")
        del st.session_state.show_data_from_neon1
        st.rerun()
    else:    
        df = conn.query("SELECT * FROM home", ttl="10minutes")
        for row in df.itertuples():
            st.write(f"Row {row.name}: {row.pet}")
         
file_upload = st.button("Click to upload a CSV file", key="file_upload")
if file_upload:
    st.subheader('Upload your CSV file')
    imported_file = st.file_uploader('', type='csv')
    if imported_file is not None:
        df = pd.read_csv(imported_file,index_col= 0)
        st.write('Data Preview:')
        st.write(df)
    else:
        st.write('Warning: Please upload a CSV file to get started.')

show_data_from_neon = st.button("Click to show data from Neon", key="show_data_from_neon1", on_click=update_session_state_for_buttons)


# Add a button to the app
# button_clicked = st.button("click me")
# if button_clicked:
#     button_clicked_count += 1
#     st.write('I love you my mangu')
#     st.write(button_clicked_count)

st.write(st.session_state)
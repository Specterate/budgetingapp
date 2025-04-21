import pandas as pd
import streamlit as st
import numpy as np
import time

button_clicked_count = 0

st.set_page_config(page_title='Budgetting App', page_icon=':moneybag:')
st.title('New Budgetting App')

st.subheader('Upload your CSV file')
imported_file = st.file_uploader('', type='csv')
if imported_file is not None:
    df = pd.read_csv(imported_file,index_col= 0)
    st.write('Data Preview:')
    st.write(df)
else:
    st.write('Warning: Please upload a CSV file to get started.', style='color: red;')


button_clicked = st.button("click me")

if button_clicked:
    button_clicked_count +=1
    while button_clicked_count >0:
        st.write('I love you my mangu')
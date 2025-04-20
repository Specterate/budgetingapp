import pandas as pd
import streamlit as st
import numpy as np
import time

st.set_page_config(page_title='Budgetting App', page_icon=':moneybag:')
st.title('New Budgetting App')

imported_file = st.file_uploader('Upload your CSV file', type='csv')
if imported_file is not None:
    df = pd.read_csv(imported_file,index_col= 0)
    st.write('Data Preview:')
    st.write(df)
else:
    st.write('Please upload a CSV file to get started.')
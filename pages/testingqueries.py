import pandas as pd
import streamlit as st
from openai import OpenAI
import os
import time
import datetime
import numpy as np

if "user_email" not in st.session_state or st.session_state.user_email is None:
    st.write("User is not logged in")
    if st.button("Go to Login Page", type="primary"):
        # Redirect to login page
        st.switch_page("Budgetingapp.py")
else:
    # Set Supabase connection and session state
    if 'conn' not in st.session_state:
        conn = st.connection("supabase",type=SupabaseConnection)
        st.session_state.conn = conn

    data = {'col1': np.random.randint(0,106,size=106)}
    df = pd.DataFrame(data)

    length = len(df)
    st.title("Testing Queries")
    st.write("Length of the DataFrame:", length)

    progress_bar = st.progress(0, text="Loading data...")
    progress_time = int(length / 4)
    count = 0
    new_progress_time = 0

    for index, row in df.iterrows():
        print(f'index: {index}, length: {length}')
        if index == (length - 1):
            progress_bar.progress(100)
            with st.spinner("Finalizing..."):
                time.sleep(2)
                progress_bar.empty()
                st.success("Loading complete!")
            break
        elif count == progress_time:
            progress_bar.progress(new_progress_time + 25)
            count = 0
            new_progress_time += 25
        else:
            count+= 1
        time.sleep(0.1)

    with st.expander("Session State", expanded=False):
        st.session_state
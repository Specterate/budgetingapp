import pandas as pd
import streamlit as st
from openai import OpenAI
import os
import time
import datetime

today = datetime.datetime.now()
this_month = today.month

date_selection = st.date_input(
    "Select the date range",
    value = [],
    format="YYYY-MM-DD",
)

submit_date = st.button("Get Data", type="primary")
if submit_date:
    st.session_state.start_date = date_selection[0]
    st.session_state.end_date = date_selection[1]
    

st.session_state



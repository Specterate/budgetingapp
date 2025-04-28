import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection


test_dict = {
    "0": {"name": "Alice", "age": 30, "location": "New York"},
    "1": {"name": "Bob", "age": 25, "location": "San Francisco"},
    "2": {"name": "Charlie", "age": 35, "location": "Chicago"},
    "3": {"name": "Diana", "age": 28, "location": "Seattle"}
}

test_df = pd.DataFrame.from_dict(test_dict, orient='index')

if "ss_df" not in st.session_state:
    st.session_state.ss_df = test_df.copy()

st.session_state.ss_df
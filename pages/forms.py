import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection


test_dict = {
    "name": ["John Doe", "Jane Smith", "Alice Johnson"],
    "age": [30, 25, 35],
    "location": ["New York", "Los Angeles", "Chicago"]
}

test_df = pd.DataFrame.from_dict(test_dict, orient='index')

st.write(test_df)
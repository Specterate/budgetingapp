import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection


test_dict = {
    "person1": {"name": "Alice", "age": 30, "location": "New York"},
    "person2": {"name": "Bob", "age": 25, "location": "San Francisco"},
    "person3": {"name": "Charlie", "age": 35, "location": "Chicago"},
    "person4": {"name": "Diana", "age": 28, "location": "Seattle"}
}

test_df = pd.DataFrame.from_dict(test_dict, orient='index')

st.write(test_df)
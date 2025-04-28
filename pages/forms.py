import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection


test_dict = [
                {"name:" : "John", "age" : 30, "city" : "New York"}, 
                {"name:" : "Jane", "age" : 25, "city" : "Los Angeles"},
                {"name:" : "Mike", "age" : 35, "city" : "Chicago"},
                {"name:" : "Emily", "age" : 28, "city" : "Houston",}
             ]

test_df = pd.DataFrame.from_dict(test_dict, orient='index')

st.write(test_df)
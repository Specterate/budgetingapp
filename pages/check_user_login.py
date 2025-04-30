import pandas as pd
import streamlit as st
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection, execute_query
from streamlit import session_state as ss

if st.session_state.user_email is not None:
    st.write("User is logged in")
else:
    st.write("User is not logged in")
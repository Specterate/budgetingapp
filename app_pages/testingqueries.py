import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection, execute_query
import datetime
import pathlib
from openai import OpenAI
import re

if "user_id" not in st.session_state:
    pass
elif st.session_state.user_id == '3ea984ac-111b-4aca-8595-2c112f4918b5':
    st.session_state.role = 'admin'
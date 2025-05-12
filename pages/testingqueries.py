import pandas as pd
import streamlit as st
from openai import OpenAI
import os

check =  st.secrets['OPENAI_API_KEY']
print(check)

# conn = st.connection("openai")
# print(conn)
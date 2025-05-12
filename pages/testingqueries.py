import pandas as pd
import streamlit as st
from openai import OpenAI
import os

st.write("Secret Key", st.secrets["openai_secret_key"])
st.write(
    "Has environment variables been set:",
    os.environ["openai_secret_key"] == st.secrets["openai_secret_key"],
)
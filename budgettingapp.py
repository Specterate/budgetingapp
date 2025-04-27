import pandas as pd
import streamlit as st
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection

st.set_page_config(page_title="Budgeting App", page_icon="💰", layout="centered")
st.title("Budgeting App")

data = {
    "Animal": ["Lion", "Crocodile", "Elephant", "Giraffe", "Penguin"],
    "Weight (kg)": [190, 430, 5000, 800, 4],
    "Is Endangered": [True, True, True, False, False],
    "Classification": ["Mammal", "Reptile", "Mammal", "Mammal", "Bird"],
    "Average Lifespan (years)": [12, 70, 70, 25, 20],
    "Habitat": ["Grassland", "Water", "Savannah", "Savannah", "Antarctica"],
}
df = pd.DataFrame(data)
st.dataframe(df)

st.session_state.df_copy = df.copy()

edited_df = st.data_editor(
    st.session_state.df_copy,
    key="my_key",
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    column_config={
        "Animal": st.column_config.TextColumn(),
        "Weight (kg)": st.column_config.NumberColumn(),
        "Is Endangered": st.column_config.CheckboxColumn(),
        "Classification": st.column_config.SelectboxColumn(
            options=["Mammal", "Reptile", "Bird"]
        ),
        "Average Lifespan (years)": st.column_config.NumberColumn(),
        "Habitat": st.column_config.SelectboxColumn(
            options=["Grassland", "Water", "Savannah", "Antarctica"]
        ),
    },
)




# https://github.com/streamlit/docs/blob/main/python/api-examples-source/data.data_editor4.py
# @st.cache_data
# def load_data():
#     data = {
#         "Animal": ["Lion", "Crocodile", "Elephant", "Giraffe", "Penguin"],
#         "Weight (kg)": [190, 430, 5000, 800, 4],
#         "Is Endangered": [True, True, True, False, False],
#         "Classification": ["Mammal", "Reptile", "Mammal", "Mammal", "Bird"],
#         "Average Lifespan (years)": [12, 70, 70, 25, 20],
#         "Habitat": ["Grassland", "Water", "Savannah", "Savannah", "Antarctica"],
#     }
#     df = pd.DataFrame(data)
#     df["Classification"] = df["Classification"].astype("category")
#     df["Habitat"] = df["Habitat"].astype("category")
#     return df


# df = load_data()

# st.data_editor(df, key="my_key", num_rows="dynamic")
# st.write("Here's the value in Session State:")
# st.write(st.session_state["my_key"])
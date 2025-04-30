import pandas as pd
import streamlit as st
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection, execute_query
from streamlit import session_state as ss

st.set_page_config(page_title="Budgeting App", page_icon="💰", layout="centered")
st.title("Budgeting App")

# Set Supabase connection and session state
if 'conn' not in st.session_state:
    conn = st.connection("supabase",type=SupabaseConnection)
    st.session_state.conn = conn

def sign_up():
    # Sign up a new user
    email = st.session_state.signup_email
    password = st.session_state.signup_password
    try:
        st.session_state.conn.auth.sign_up(dict(email=email, password=password))
        st.success("Sign up successful!")
    except Exception as e:
        st.error(f"Error signing up: {e}")

def sign_in():
    # Sign in an existing user
    email = st.session_state.signin_email
    password = st.session_state.signin_password
    try:
        st.session_state.conn.auth.sign_in(dict(email=email, password=password))
        st.success("Sign in successful!")
    except Exception as e:
        st.error(f"Error signing in: {e}")

col1, col2 = st.columns(2)
with col1:
    with st.form(key='signup_form'):
        st.text_input("Email", key='signup_email')
        st.text_input("Password", type="password", key='signup_password')
        st.form_submit_button("Sign Up", on_click=sign_up)
with col2:
    with st.form(key='signin_form'):
        st.text_input("Email", key='signin_email')
        st.text_input("Password", type="password", key='signin_password')
        st.form_submit_button("Sign In", on_click=sign_in)
    

# # Query categories table from supabase and convert to DataFrame
# if 'get_category_data_df' not in st.session_state:
#     get_category_data_df = pd.DataFrame.from_dict(st.session_state.conn.table("categories").select("*").execute().data)
#     st.session_state.get_category_data_ss = get_category_data_df

# ----- This works for session state with pandas dataframe -----
# def update_df():    
#     if st.session_state['editor']['edited_rows']:
#         for index, changes in st.session_state['editor']['edited_rows'].items():
#             for col, value in changes.items():
#                 st.session_state['df'].loc[index, col] = value
#     st.session_state['df']

# if 'df' not in st.session_state:
#     st.session_state['df'] = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

# st.write("This is a editable dataframe")
# st.data_editor(st.session_state['df'], on_change=update_df, key="editor", num_rows="dynamic")

# ===================



# Create a variable to hold the counter. See to it
# that the key `cnt` is not yet in session state.
# Intialize it with a value of 0.
# if 'cnt' not in ss:
#     ss.cnt = 0  # okay we are good


# def prev_callback():
#     ss.cnt -= 1  # decrement properly


# def next_callback():
#     ss.cnt += 1  # increment properly


# left, center, right = st.columns([1, 1, 1], gap='small')

# left.button('Previous', type='secondary', on_click=prev_callback)
# center.button(f'{ss.cnt}', type='primary')
# right.button('Next', type='secondary', on_click=next_callback)



# data = {
#     "Animal": ["Lion", "Crocodile", "Elephant", "Giraffe", "Penguin"],
#     "Weight (kg)": [190, 430, 5000, 800, 4],
#     "Is Endangered": [True, True, True, False, False],
#     "Classification": ["Mammal", "Reptile", "Mammal", "Mammal", "Bird"],
#     "Average Lifespan (years)": [12, 70, 70, 25, 20],
#     "Habitat": ["Grassland", "Water", "Savannah", "Savannah", "Antarctica"],
# }
# df = pd.DataFrame(data)
# st.write("Original DataFrame")
# st.dataframe(df)

# st.session_state.df_copy = df.copy()

# edited_df = st.data_editor(
#     df,
#     num_rows="dynamic",
#     use_container_width=True,
#     hide_index=True,
#     column_config={
#         "Animal": st.column_config.TextColumn(),
#         "Weight (kg)": st.column_config.NumberColumn(),
#         "Is Endangered": st.column_config.CheckboxColumn(),
#         "Classification": st.column_config.SelectboxColumn(
#             options=["Mammal", "Reptile", "Bird"]
#         ),
#         "Average Lifespan (years)": st.column_config.NumberColumn(),
#         "Habitat": st.column_config.SelectboxColumn(
#             options=["Grassland", "Water", "Savannah", "Antarctica"]
#         ),
#     },
# )




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
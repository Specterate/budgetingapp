import pandas as pd
import streamlit as st
import numpy as np
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from st_supabase_connection import SupabaseConnection, execute_query
from streamlit import session_state as ss
import pathlib

st.set_page_config(page_title="Budgeting App", page_icon="💰", layout='wide', initial_sidebar_state='expanded')
st.title("Budgeting App")

# Function to load CSS from the 'assets' folder
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load the external CSS
css_path = pathlib.Path('style.css')
load_css(css_path)

# Examples on how to run CSS styling
# https://github.com/Sven-Bo/streamit-css-styling-demo/blob/main/assets/styles.css
# https://www.youtube.com/watch?v=jbJpAdGlKVY

# Set Supabase connection and session state
st.session_state.conn = st.connection("supabase",type=SupabaseConnection)

def sign_up(email, password):
    try:
        user = st.session_state.conn.auth.sign_up({"email": email, "password": password})
        return user
    except Exception as e:
        st.error(f"Registration failed: {e}")

def sign_in(email, password):
    try:
        user = st.session_state.conn.auth.sign_in_with_password({"email": email, "password": password})
        return user
    except Exception as e:
        st.error(f"Login failed: {e}")

def sign_out():
    try:
        st.session_state.conn.auth.sign_out()
        st.session_state.user_email = None
        st.rerun()
    except Exception as e:
        st.error(f"Logout failed: {e}")

def main_app(user_email):
    st.html("<p style='font-size:20px; text-align:center'>You are logged in! \n</p>")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Go to Dashboard", type="secondary", use_container_width=True, key="dashboard_button"):
            st.switch_page("pages/01_Dashboard.py")
    with col2:
        if st.button("Go to Category", type="secondary", use_container_width=True):
            st.switch_page("pages/02_Categories.py")
    with col3:
        if st.button("Go to Import/Export", type="secondary", use_container_width=True):
            st.switch_page("pages/03_ImportCSV.py")
    col4, col5, col6 = st.columns(3)
    with col5:
        if st.button("Logout", type="primary", use_container_width=True):
            sign_out()

def auth_screen():
    option = st.selectbox("Choose an action:", ["Login", "Sign Up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if option == "Sign Up" and st.button("Register"):
        user = sign_up(email, password)
        if user and user.user:
            st.success("Registration successful. Please log in.")

    if option == "Login" and st.button("Login"):
        user = sign_in(email, password)
        if user and user.user:
            st.session_state.user_email = user.user.email
            st.success(f"Welcome back, {email}!")
            st.rerun()

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if st.session_state.user_email:
    main_app(st.session_state.user_email)
else:
    auth_screen()

# Check if user is logged in
if "user_email" in st.session_state and st.session_state.user_email:
    with st.expander("Session State", expanded=False):
        st.session_state
import pandas as pd
import streamlit as st
from openai import OpenAI
import os
import time

def update_de():
    pass

# Define the menu items data
menu_data = {
    "Name": ["Burger", "Salad", "Pizza", "Pasta", "Soda"],
    "Type": ["Main Course", "Appetizer", "Main Course", "Main Course", "Beverage"]
}

# Create a pandas DataFrame
menu_df = pd.DataFrame(menu_data)

food_type_dict = ["Main Course", "Appetizer", "Beverage"]

# Display the DataFrame
st.data_editor(menu_df,
                column_config={
                     "Name": st.column_config.TextColumn("Name", help="Name of the food item"),
                     "Type": st.column_config.SelectboxColumn("Type", options=food_type_dict, help="Type of the food item")
                },
                hide_index=True,
                use_container_width=True,
                num_rows="dynamic",
                key="menu_df",
                on_change=update_de)

import pandas as pd
import streamlit as st
from openai import OpenAI
import os
import time

print('Application started -----------------------------------------------')

try:
    open_ai_key_value = st.secrets["openai_key"]["openai_secret_key"]
    client = OpenAI(api_key=open_ai_key_value)
except KeyError:
    st.error("OpenAI key not found in secrets. Please set it up in the Streamlit secrets manager.")
    st.stop()
def refresh_dashboard():
    for key in st.session_state.keys():
        if key == 'user_email':
            pass
        else:
            del st.session_state[key]

def openai_classification(desc):
    print("desc")
    print(desc)
    prompt_cat_list = "House rent, Supermarket, Internet home, Mobile phone, Gas, Electricity, Bank charges (card, taxes), Online services, Restaurants, Delivery, Aperitifs/bars, Shopping for Home, Clothes, Health, Courses, Technology, Transportation (plane, bus, subway, car)."

    content_system = ("I would like to classify my expenses using specific categories. In input you will have the list of categories and the description of an expense. Please associate a category to the expense. "
"Please only respond with the exact name of the category listed and nothing else. " + "Categories: \n") + prompt_cat_list


    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": content_system},
            {"role": "user", "content": "Expense description: " + str(desc)}]
)      
    data = completion.choices[0].message
    print("data")
    print(data.content)
    return data.content
    

with st.sidebar:
    st.button("Refresh Page", type="primary", use_container_width=True, on_click=refresh_dashboard)


# uploaded_file = st.file_uploader("Please ensure the file is in CSV format and contains the required columns as Date, Description, Amount", label_visibility ="visible", help="Upload a CSV file with the required columns", key='uploaded_file')
# if uploaded_file is not None:
#     try:
#         file_import_df = pd.read_csv(uploaded_file, usecols=['Date', 'Description', 'Amount'])
#         file_import_df['Category'] = 'Uncategorized'
#     except ValueError as e:
#         print(f"Error reading file: {e}")
#         st.error("Error reading file, please ensure the following columns are present - Date, Description, Amount")
#         st.stop()

#     print('file_import_df')
#     print(file_import_df)

#     for index, row in file_import_df.iterrows():
#         label = str(openai_classification(row['Description']))
#         print(label)
#         # file_import_df.at[index, 'Description'] = label
#         print(str(row['Description']) + ' - ' + label)
#         time.sleep(0.5)

capture_text =  st.text_input("Enter a description", key="description_input")
if capture_text:
    label = str(openai_classification(capture_text))
    print(label)
    st.write("Label: ", label)
    time.sleep(0.5)

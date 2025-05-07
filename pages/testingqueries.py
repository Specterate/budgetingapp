import pandas as pd
import streamlit as st


# @st.cache_data
data_df = pd.DataFrame(
        {
            "category": [
                "📊 Data Exploration",
                "📈 Data Visualization",
                "🤖 LLM",
                "📊 Data Exploration",
            ],
            "subcategory": [
                "Data Cleaning",
                "Data Analysis",
                "Text Generation",
                "Data Transformation",
            ],
            "description": [
                "Pandas",
                "Matplotlib",
                "OpenAI",
                "NumPy",
            ],
        }
    )

listofoptions = [
                "📊 Data Exploration",
                "📈 Data Visualization",
                "🤖 LLM",
                "Testing Data",
            ]


st.data_editor(
    data_df,
    num_rows="dynamic",
    use_container_width=True,
    key="data_editor",
    column_config={
        "category": st.column_config.SelectboxColumn(
            "App Category",
            help="The category of the app",
            width="medium",
            options=listofoptions,
            required=True,
        ),
        "subcategory": st.column_config.SelectboxColumn(
            "Subcategory",
            help="The subcategory of the app",
            width="medium",
            options=["Data Cleaning", "Data Analysis", "Text Generation", "Data Transformation"],
            required=True,
        ),
        "description": st.column_config.SelectboxColumn(
            "Description",
            help="The description of the app",
            width="medium",
            options=["Pandas", "Matplotlib", "OpenAI", "NumPy"],
            required=True,
        ),
    },
    hide_index=True,
)
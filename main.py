import streamlit as st
import pandas as pd
import os
from page_1 import *

# Ensure tasks_df persists across reruns
if "tasks_df" not in st.session_state:
    st.session_state.tasks_df = pd.DataFrame(columns=["Task", "Start Date", "Frequency (days)", "Day of Month"])

# Function to load tasks from an Excel file
def load_tasks(file):
    df = pd.read_excel(file)
    df['Start Date'] = df['Start Date'].apply(lambda x: x.date())
    return df

uploaded_file = st.sidebar.file_uploader("Upload an Excel file", type=["xlsx"])
if uploaded_file:
    st.session_state.tasks_df = load_tasks(uploaded_file)
    st.sidebar.write("Tasks loaded successfully!")

# Load default tasks file if it exists
default_file_path = "tasks.xlsx"
if os.path.exists(default_file_path):
    st.session_state.tasks_df = load_tasks(default_file_path)
    st.sidebar.write("Default tasks loaded successfully!")
    default_file_loaded = True
else:
    default_file_loaded = False


# Streamlit app
logo_path = "logo.JPEG"

st.image("generated_3.jpg", use_container_width=True, width = 15)
st.write('<p style="font-size: 24px; font-family: Raleway , sans-serif; color: #000; font-weight: bold; text-align: center;">'
        'GUERLAIN SCHEDULER'
        '</p>',
        unsafe_allow_html=True
    )

today = datetime.date.today()
year = st.sidebar.selectbox("Select Year", range(today.year, today.year + 5), index=0)
month = st.sidebar.selectbox("Select Month", range(1, 13), index=today.month - 1)

fill_calendar(year, month)

st.write("## Download Tasks")
excel_data = convert_df_to_excel(st.session_state.tasks_df)
st.download_button(
    label="Download Updated Tasks",
    data=excel_data,
    file_name="updated_tasks.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

import streamlit as st
import pandas as pd
import calendar
import datetime
import io
import os

# Ensure tasks_df persists across reruns
if "tasks_df" not in st.session_state:
    st.session_state.tasks_df = pd.DataFrame(columns=["Task", "Start Date", "Frequency (days)", "Day of Month"])

# Function to load tasks from an Excel file
def load_tasks(file):
    df = pd.read_excel(file)
    df['Start Date'] = df['Start Date'].apply(lambda x: x.date())
    return df

# Load default tasks file if it exists
# Load default tasks file if it exists
default_file_path = "tasks.xlsx"
if os.path.exists(default_file_path):
    st.session_state.tasks_df = load_tasks(default_file_path)
    st.sidebar.write("Default tasks loaded successfully!")
    default_file_loaded = True
else:
    default_file_loaded = False
    
# Function to generate the calendar
def generate_calendar(year, month):
    return calendar.monthcalendar(year, month)

# Streamlit app
#st.title("Recurring Event Management")

# Code SVG logo
logo_path = "logo.JPEG"

# svg_code = """
# <svg width="120" height="16" viewBox="0 0 367.8 50.5">
#     <style>
#         .st0 { fill: #010101; }
#     </style>
#     <g>
#         <path style="fill:#010101;" d="M 192.2 49.3 l -14.9 -16.2 h -7.5 v 16.2 h -7.7 V 1.2 h 20.3 c 8.8 0 15.9 7.1 15.9 15.9 c 0 11.9 -10.2 15.2 -11.6 15.4 c 0 0 15.3 16.8 15.3 16.8 H 192.2 Z M 169.8 25.4 h 12.6 c 4.5 0 8.2 -3.7 8.2 -8.2 s -3.7 -8.2 -8.2 -8.2 h -12.6 V 25.4 Z"></path>
#         <path style="fill:#010101;" d="M25.1,50.5
# 		C11,50.5,0,39.4,0,25.3S11.1,0,25.2,0c8.3,0,15.2,3.4,20,9.7l-6.5,4.8c-3.1-4.4-7.9-6.8-13.5-6.8c-9.6,0-16.8,7.4-16.8,17.5
# 		c0,10.2,7.1,17.5,16.7,17.5l0.2,0c8.3,0,14.5-4.9,16.1-12.7l0.1-0.4l-14.7,0l0-7.7l23.3,0l0,3.8c0,6.7-2.4,12.6-7.1,17.4
# 		c-4.6,4.7-10.9,7.3-17.7,7.3L25.1,50.5z"></path>
#         <path style="fill:#010101;" d="M82.4,50.5
# 		c-11.5,0-20.9-9.4-20.9-20.9V1.2h7.7v28.4c0,7.3,5.9,13.3,13.3,13.3c7.3,0,13.3-5.9,13.3-13.3V1.2h7.7v28.4
# 		C103.3,41.1,93.9,50.5,82.4,50.5"></path>
#         <polygon style="fill:#010101;" points="116.1,49.3
# 		116.1,1.2 149.1,1.2 149.1,8.9 123.8,8.9 123.8,21.4 147.2,21.4 147.2,29.1 123.8,29.1 123.8,41.6 149.1,41.6 149.1,49.3 	"></polygon>
#         <polygon style="fill:#010101;" points="212.9,49.3
# 		212.9,1.2 220.5,1.2 220.5,41.6 241.7,41.6 241.7,49.3 	"></polygon>
#         <path style="fill:#010101;" d="M286.6,49.3L282,38.1
# 		h-21.4l-4.5,11.2h-8.3l19.3-48.1h8.4l19.3,48.1H286.6z M263.6,30.5H279L271.3,11L263.6,30.5z"></path>
#         <rect x="304" y="1.2" style="fill:#010101;" width="7.7" height="48.1"></rect>
#         <polygon style="fill:#010101;" points="359.8,49.3
# 		333.3,13.7 333.3,49.3 325.6,49.3 325.6,1.2 333.6,1.2 360.1,36.9 360.1,1.2 367.8,1.2 367.8,49.3 	"></polygon>
#     </g>
# </svg>
# """
st.image("generated_3.jpg", use_container_width=True, width = 15)
st.write('<p style="font-size: 24px; font-family: Raleway , sans-serif; color: #000; font-weight: bold; text-align: center;">'
        'GUERLAIN SCHEDULER'
        '</p>',
        unsafe_allow_html=True
    )
# col1, col2 = st.columns([1, 4])
# with col1:
#     st.image(logo_path, width = 25)

# with col2:
#     #st.markdown(svg_code, unsafe_allow_html=True)
#     st.write(
#         '<p style="font-size: 24px; font-family: Raleway , sans-serif; color: #000; font-weight: bold; text-align: center;">'
#         'GUERLAIN SCHEDULER'
#         '</p>',
#         unsafe_allow_html=True
#     )

# Sidebar for uploading an Excel file
uploaded_file = st.sidebar.file_uploader("Upload an Excel file", type=["xlsx"])
if uploaded_file:
    st.session_state.tasks_df = load_tasks(uploaded_file)
    st.sidebar.write("Tasks loaded successfully!")

# Sidebar to select year and month
today = datetime.date.today()
year = st.sidebar.selectbox("Select Year", range(today.year, today.year + 5), index=0)
month = st.sidebar.selectbox("Select Month", range(1, 13), index=today.month - 1)

# Generate the calendar for the selected month
cal = generate_calendar(year, month)
st.write(f"### {calendar.month_name[month]} {year}")

# Prepare task data to be displayed on the calendar
task_dates = []

# Collect task dates from tasks_df
for _, row in st.session_state.tasks_df.iterrows():
    start_date = row["Start Date"]
    frequency = row["Frequency (days)"]
    day_of_month = row["Day of Month"]

    # If the task has a frequency, generate multiple dates
    if pd.notna(frequency):
        current_date = start_date
        while current_date <= datetime.date(year, month, calendar.monthrange(year, month)[1]):
            #if current_date.year == year and current_date.month == month:
            task_dates.append((current_date.day, row["Task"]))
            current_date += datetime.timedelta(days=frequency)

    # If the task is based on a specific day of the month
    if pd.notna(day_of_month):
        if start_date.year < year or (start_date.year == year and start_date.month <= month):
            task_dates.append((day_of_month, row["Task"]))

# Debugging: Print task dates to verify the tasks are being added
# st.write("### Debug - Task Dates:")
# st.write(task_dates)

# Define colors for task bands
task_colors = [
    "#FFCDD2",  # Red
    "#FFECB3",  # Yellow
    "#C8E6C9",  # Green
    "#BBDEFB",  # Blue
    "#D1C4E9",  # Purple
    "#FFAB91",  # Orange
    "#BCAAA4",  # Brown
]

# Create HTML for the calendar
calendar_html = '<table style="width: 100%; border-collapse: collapse;">'
calendar_html += "<thead><tr>"

# Add day names
for day_name in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
    calendar_html += f'<th style="text-align: center; padding: 5px; border: 1px solid #ddd;">{day_name}</th>'
calendar_html += "</tr></thead><tbody>"

# Create rows for the calendar (each week of the month)
for week in cal:
    calendar_html += "<tr>"
    for day in week:
        if day == 0:
            calendar_html += '<td style="text-align: center; padding: 5px; border: 1px solid #ddd;"></td>'  # Empty cell for days outside of the current month
        else:
            # Find tasks for this day
            tasks_on_day = [task for task_day, task in task_dates if task_day == day]
            task_bands = ""
            if tasks_on_day:
                # Assign colors to each task
                task_bands = "<br>".join([f'<div style="background-color: {task_colors[i % len(task_colors)]}; padding: 2px; border-radius: 5px; margin: 2px 0;">{task}</div>' for i, task in enumerate(tasks_on_day)])
            calendar_html += f'<td style="text-align: center; padding: 5px; border: 1px solid #ddd; height: 100px;">{day}<br>{task_bands}</td>'
    calendar_html += "</tr>"

calendar_html += "</tbody></table>"

# Display the calendar using markdown
st.markdown(calendar_html, unsafe_allow_html=True)

# Display the tasks uploaded in the Excel file (tasks_df)
st.write("## Scheduled Tasks")
st.dataframe(st.session_state.tasks_df)

# Function to convert df to Excel and download
def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Tasks")
    return output.getvalue()

#Download button
st.write("## Download Tasks")
excel_data = convert_df_to_excel(st.session_state.tasks_df)
st.download_button(
    label="Download Updated Tasks",
    data=excel_data,
    file_name="updated_tasks.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
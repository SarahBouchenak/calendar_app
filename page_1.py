import streamlit as st
import pandas as pd
import calendar
import datetime
import io
    
# Function to generate the calendar
def generate_calendar(year, month):
    cal = calendar.monthcalendar(year, month)
    return cal

def fill_calendar(year, month, group):

    st.write(f"### {calendar.month_name[month]} {year}")
    cal = generate_calendar(year, month)
    # Prepare task data to be displayed on the calendar
    task_dates = []

    # Collect task dates from tasks_df
    tasks_df = st.session_state.tasks_df.query('GROUP==@group')
    tasks_df = tasks_df.sort_values(by="Hour")
    for _, row in tasks_df.iterrows():
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
                calendar_html += f'<td style="text-align: center; padding: 5px; border: 1px solid #ddd; height: 100px; vertical-align: top;"><div style="height: 20px;"><strong>{day}</strong></div><div>{task_bands}</div></td>'
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
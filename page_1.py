import streamlit as st
import pandas as pd
import calendar
import datetime
import io

# Function to generate the calendar
def generate_calendar(year, month):
    cal = calendar.monthcalendar(year, month)
    return cal

def generate_dates(year, month, group, task_colors):
    st.write(f"### {calendar.month_name[month]} {year}")
    # Prepare task data to be displayed on the calendar
    task_dates = []

    # Collect task dates from tasks_df
    tasks_df = st.session_state.tasks_df.query('GROUP==@group')
    tasks_df = tasks_df.sort_values(by="Hour")
    for _, row in tasks_df.iterrows():
        start_date = row["Start Date"]
        frequency = row["Frequency (days)"]
        day_of_month = row["Day of Month"]
        task_name = row["Task"]
        task_hour = row["Hour"]
        # If the task has a frequency, generate multiple dates
        if pd.notna(frequency):
            current_date = start_date
            while current_date <= datetime.date(year, month, calendar.monthrange(year, month)[1]):
                if current_date.year == year and current_date.month == month:
                    task_dates.append((current_date.day, task_name, task_hour))
                current_date += datetime.timedelta(days=frequency)

        # If the task is based on a specific day of the month
        if pd.notna(day_of_month):
            if start_date.year < year or (start_date.year == year and start_date.month <= month):
                task_dates.append((day_of_month, task_name, task_hour))

    return task_dates

def fill_calendar(year, month, group, task_colors):
    cal = generate_calendar(year, month)
    task_dates = generate_dates(year, month, group, task_colors)
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
                tasks_on_day = [(task_name, task_hour) for task_day, task_name, task_hour in task_dates if task_day == day]
                task_bands = ""
                if tasks_on_day:
                    # Assign colors to each task and add tooltip with task name and hour
                    task_bands = "<br>".join([f'<div title="at {task_hour}" style="background-color: {task_colors[i % len(task_colors)]}; padding: 2px; border-radius: 5px; margin: 2px 0;">{task_name}</div>' for i, (task_name, task_hour) in enumerate(tasks_on_day)])
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
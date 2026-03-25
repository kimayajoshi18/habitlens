import streamlit as st
from datetime import date 
import pandas as pd 

#Title
st.title("HabitLens")
st.write("Track your habits and discover behavior patterns over time!")

#Today's date
today = date.today()
csv_file = "data/habits.csv"
st.subheader(f"Today's Entry: {today}")

#Habits to be tracked
gym = st.checkbox("Gym")
study = st.checkbox("Studying")
sleep = st.checkbox("Sleep Goal Met")
ate_out = st.checkbox("Ate Out")
ate_sweets = st.checkbox("Ate Sweets")

#Saving habits
if st.button("Save Today's Entry"):
    new_entry = {
        "date": str(today),
        "gym": gym,
        "studying": study,
        "sleep_goal": sleep,
        "ate_out": ate_out,
        "ate_sweets": ate_sweets
    }
    new_entry_df = pd.DataFrame([new_entry])

    try:
        existing_data = pd.read_csv(csv_file)
        existing_data = existing_data[existing_data["date"] != str(today)]
        updated_data = pd.concat([existing_data, new_entry_df], ignore_index=True)
    except FileNotFoundError:
        updated_data = new_entry_df
    
    updated_data.to_csv(csv_file, index=False)
    st.success("Today's habits saved successfully!")

#Dashboard
st.subheader("Saved Habit History")
try:
    habit_data = pd.read_csv(csv_file)
    #most recent entry at top
    habit_data = habit_data.sort_values(by="date", ascending=False)
    st.dataframe(habit_data)
except FileNotFoundError:
    st.info("No habit data saved yet.")

#Display metrics
st.subheader("Habit Dashboard Metrics")

try:
    habit_data = pd.read_csv(csv_file)
    total_days = len(habit_data)

    # Positive completion percentages
    gym_pct = round(habit_data["gym"].mean() * 100, 1)
    studying_pct = round(habit_data["studying"].mean() * 100, 1)
    sleep_pct = round(habit_data["sleep_goal"].mean() * 100, 1)

    # Negative habits re-written positively
    sweets_pct = round((~habit_data["ate_sweets"]).mean() * 100, 1)
    ate_out_pct = round((~habit_data["ate_out"]).mean() * 100, 1)

    col1, col2, col3 = st.columns(3)
    col1.metric("Gym Completion", f"{gym_pct}%")
    col2.metric("Studying Completion", f"{studying_pct}%")
    col3.metric("Sleep Goal Completion", f"{sleep_pct}%")
    col4, col5 = st.columns(2)
    col4.metric("Days Without Sweets", f"{sweets_pct}%")
    col5.metric("Days Without Eating Out", f"{ate_out_pct}%")
    st.write(f"**Total Days Tracked:** {total_days}")
except FileNotFoundError:
    st.info("No habit data to display metrics yet.")
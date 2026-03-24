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
    st.info("No habit data saved yet")
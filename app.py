import streamlit as st
from datetime import date, timedelta
import pandas as pd 

st.set_page_config(page_title="HabitLens", page_icon="🧠", layout="wide")

#Title
st.title("🧠 HabitLens")
st.subheader("Track your habits and discover behavior patterns over time!")
st.divider()

#Today's date
st.subheader("📋 Daily Habit Check-In")
today = date.today()
csv_file = "data/habits.csv"
st.subheader(f"Today's Entry: {today}")

#Habits to be tracked
col1, col2 = st.columns(2)
with col1:
    gym = st.checkbox("💪 Gym")
    study = st.checkbox("📚 Studying")
    sleep = st.checkbox("😴 Sleep goal met")
with col2:
    ate_out = st.checkbox("🍽️ Ate out")
    ate_sweets = st.checkbox("🍭 Ate sweets")

#Saving habits
st.markdown("###")
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

st.divider()
st.subheader("🧪 Sample Data Generator")
st.caption("Creating realistic past habit data to test charts and behavior insights.")
if st.button("✨ Generate 30 Days of Sample Data"):
    sample_rows = []

    # Load existing data if it exists
    try:
        existing_data = pd.read_csv(csv_file)
        existing_dates = set(existing_data["date"].astype(str))
    except FileNotFoundError:
        existing_data = pd.DataFrame()
        existing_dates = set()

    # Generate last 30 days
    for i in range(30):
        sample_date = today - timedelta(days=i)
        sample_date_str = str(sample_date)

        # Skip if date already exists
        if sample_date_str in existing_dates:
            continue

        weekday = sample_date.weekday()  # Monday=0, Sunday=6
        is_weekend = weekday >= 5

        # Realistic behavior patterns
        gym = (not is_weekend and i % 3 != 0) or (is_weekend and i % 5 == 0)
        studying = (not is_weekend and i % 4 != 0) or (is_weekend and i % 6 == 0)
        sleep_goal = i % 4 != 0
        ate_out = is_weekend or (i % 7 == 0)
        ate_sweets = is_weekend or (i % 5 == 0)

        sample_rows.append({
            "date": sample_date_str,
            "gym": gym,
            "studying": studying,
            "sleep_goal": sleep_goal,
            "ate_out": ate_out,
            "ate_sweets": ate_sweets
        })

    if sample_rows:
        sample_df = pd.DataFrame(sample_rows)

        if existing_data.empty:
            sample_df.to_csv(csv_file, index=False)
        else:
            combined_data = pd.concat([existing_data, sample_df], ignore_index=True)
            combined_data = combined_data.sort_values(by="date")
            combined_data.to_csv(csv_file, index=False)

        st.success(f"Added {len(sample_rows)} days of sample data!")
    else:
        st.info("All sample dates already exist. No new sample data added.")
st.divider()

#Dashboard
st.subheader("📆 Saved Habit History")
try:
    habit_data = pd.read_csv(csv_file)
    #most recent entry at top
    habit_data = habit_data.sort_values(by="date", ascending=False)
    st.dataframe(habit_data, width="stretch")
except FileNotFoundError:
    st.info("No habit data saved yet.")
st.divider()

#Display metrics
st.subheader("📊 Habit Dashboard Metrics")

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
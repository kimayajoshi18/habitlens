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

st.divider()
st.subheader("📈 Habit Visualizations")
try:
    habit_data = pd.read_csv(csv_file)
    chart_data = pd.DataFrame({
        "Habit": [
            "Gym",
            "Studying",
            "Sleep Goal",
            "No Sweets",
            "No Eating Out"
        ],
        "Completion %": [
            habit_data["gym"].mean() * 100,
            habit_data["studying"].mean() * 100,
            habit_data["sleep_goal"].mean() * 100,
            (~habit_data["ate_sweets"]).mean() * 100,
            (~habit_data["ate_out"]).mean() * 100
        ]
    })
    st.write("### Overall Habit Completion Rates")
    st.bar_chart(chart_data.set_index("Habit"))
except FileNotFoundError:
    st.info("No habit data available for charts yet.")

try:
    habit_data = pd.read_csv(csv_file)
    habit_data["date"] = pd.to_datetime(habit_data["date"])
    habit_data = habit_data.sort_values(by="date")

    # Convert negative habits into positive behavior scores
    habit_data["no_sweets"] = ~habit_data["ate_sweets"]
    habit_data["no_eating_out"] = ~habit_data["ate_out"]

    # Count how many positive habits were completed each day + score out of 5
    habit_data["positive_habit_score"] = (
        habit_data["gym"].astype(int) +
        habit_data["studying"].astype(int) +
        habit_data["sleep_goal"].astype(int) +
        habit_data["no_sweets"].astype(int) +
        habit_data["no_eating_out"].astype(int)
    )
    trend_data = habit_data[["date", "positive_habit_score"]].set_index("date")
    st.write("### Daily Positive Habit Score Over Time")
    st.line_chart(trend_data)
except FileNotFoundError:
    st.info("No habit data available for trend chart yet.")

st.divider()
st.subheader("🧐 Behavioral Insights")
try:
    habit_data = pd.read_csv(csv_file)

    # Make sure date is datetime
    habit_data["date"] = pd.to_datetime(habit_data["date"])

    # Add weekday/weekend label
    habit_data["is_weekend"] = habit_data["date"].dt.weekday >= 5

    # Positive-framed habit completion rates
    habit_rates = {
        "Gym": habit_data["gym"].mean() * 100,
        "Studying": habit_data["studying"].mean() * 100,
        "Sleep Goal": habit_data["sleep_goal"].mean() * 100,
        "No Sweets": (~habit_data["ate_sweets"]).mean() * 100,
        "No Eating Out": (~habit_data["ate_out"]).mean() * 100
    }

    # Strongest and weakest habits
    strongest_habit = max(habit_rates, key=habit_rates.get)
    weakest_habit = min(habit_rates, key=habit_rates.get)

    # Create a daily positive score for weekday/weekend comparison
    habit_data["no_sweets"] = ~habit_data["ate_sweets"]
    habit_data["no_eating_out"] = ~habit_data["ate_out"]

    habit_data["positive_habit_score"] = (
        habit_data["gym"].astype(int) +
        habit_data["studying"].astype(int) +
        habit_data["sleep_goal"].astype(int) +
        habit_data["no_sweets"].astype(int) +
        habit_data["no_eating_out"].astype(int)
    )

    weekday_avg = habit_data[~habit_data["is_weekend"]]["positive_habit_score"].mean()
    weekend_avg = habit_data[habit_data["is_weekend"]]["positive_habit_score"].mean()

    # Display insights
    st.markdown(
    f"<p style='font-size:22px;'>✅ <b>Strongest Habit:</b> {strongest_habit} ({habit_rates[strongest_habit]:.1f}%)</p>",
    unsafe_allow_html=True
    )
    st.markdown(
        f"<p style='font-size:22px;'>⚠️ <b>Habit to Improve:</b> {weakest_habit} ({habit_rates[weakest_habit]:.1f}%)</p>",
        unsafe_allow_html=True
    )
    if weekday_avg > weekend_avg:
        st.markdown(
            "<p style='font-size:22px;'>📅 <b>Insight:</b> You tend to be more consistent on weekdays than weekends! Keep going!</p>",
            unsafe_allow_html=True
        )
    elif weekend_avg > weekday_avg:
        st.markdown(
            "<p style='font-size:22px;'>🎉 <b>Insight:</b> You tend to be more consistent on weekends than weekdays. Keep at it!</p>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<p style='font-size:22px;'>⚖️ <b>Insight:</b> Your habits are equally consistent on weekdays and weekends! You're doing great!</p>",
            unsafe_allow_html=True
        )
except FileNotFoundError:
    st.info("No habit data available for insights yet.")
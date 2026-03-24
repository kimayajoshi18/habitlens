import streamlit as st
from datetime import date 
st.title("HabitLens")
st.write("Track your habits and discover behavior patterns over time!")

today = date.today()
st.subheader(f"Today's Entry: {today}")

gym = st.checkbox("Gym")
studying = st.checkbox("Studying")
sleep_goal = st.checkbox("Sleep Goal Met")
ate_out = st.checkbox("Ate Out")
ate_sweets = st.checkbox("Ate Sweets")

if st.button("Save Today's Entry"):
    st.success("Today's habits saved successfully!")
import streamlit as st
from logic.graph import plan_trip_streaming

st.title("Agentic Trip Planner")

user_query = st.text_input("Where do you want to go, and for how long?")

if st.button("Plan my trip"):
    st.write(f"You asked: {user_query}")

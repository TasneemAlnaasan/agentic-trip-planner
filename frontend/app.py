import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import streamlit as st
from logic.graph import plan_trip_streaming

st.title("Agentic Trip Planner")

user_query = st.text_input("Where do you want to go, and for how long?")

if st.button("Plan my trip"):
    with st.status("Planning your trip...") as status:
        for step in plan_trip_streaming(user_query):
            node_name = list(step.keys())[0]

            if node_name == "planner":
                status.update(label="Gathering weather, places, and prices...")
            elif node_name == "evaluator":
                status.update(label="Checking if the plan is good enough...")
            elif node_name == "replanner":
                status.update(label="Not quite right — trying again...")
            elif node_name == "final_composer":
                status.update(label="Finalizing your itinerary...", state="complete")

            final_step = step

        final_itinerary = final_step["final_composer"]["itinerary_text"]

    st.markdown(final_itinerary)

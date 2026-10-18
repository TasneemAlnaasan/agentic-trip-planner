import sys
import os
import streamlit as st
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic.graph import plan_trip_streaming


st.set_page_config(
    page_title="Agentic Trip Planner",
    page_icon="✈️",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #FFF5E1 0%, #E8F4F8 100%);
    }
    h1 {
        color: #2E5C87;
    }
    .stButton button {
        background: linear-gradient(90deg, #FF8C42 0%, #FF6B6B 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: bold;
        font-size: 16px;
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #FF6B6B 0%, #FF8C42 100%);
        transform: scale(1.02);
    }
    .stTextInput input {
        border-radius: 15px;
        border: 2px solid #FF8C42;
    }
    </style>
""", unsafe_allow_html=True)


st.title("✈️ Agentic Trip Planner")
st.caption("🌍 Note: Weather forecasts are most accurate for the first 16 days of your trip; later days use general seasonal expectations.")

user_query = st.text_input("🗺️ Where do you want to go, and for how long?")

if st.button("🚀 Plan my trip"):
    with st.status("Planning your trip...") as status:
        for step in plan_trip_streaming(user_query):
            node_name = list(step.keys())[0]

            if node_name == "planner":
                status.update(label="🔍 Gathering weather, places, and prices...")
            elif node_name == "evaluator":
                status.update(label="✅ Checking if the plan is good enough...")
            elif node_name == "replanner":
                status.update(label="🔄 Not quite right — trying again...")
            elif node_name == "final_composer":
                status.update(label="🎉 Finalizing your itinerary...", state="complete")

            final_step = step

        final_itinerary = final_step["final_composer"]["itinerary_text"]

    st.markdown(final_itinerary)

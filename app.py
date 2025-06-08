import streamlit as st
from diet_chatbot import get_diet_plan  # You’ll create this file too

st.title("🥗 AI Diet Chatbot")
st.write("Describe your fitness goal and food preference.")

goal = st.text_input("🎯 Your Goal (e.g., weight loss, muscle gain)")
food_type = st.text_input("🍽️ Food Type (e.g., veg, high protein)")

if st.button("Get My Diet Plan"):
    if goal and food_type:
        plan = get_diet_plan(goal, food_type)
        st.success(plan)
    else:
        st.warning("Please fill out both fields.")

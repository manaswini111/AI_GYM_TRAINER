import streamlit as st
from diet_chatbot import get_diet_recommendation

st.title("🏋️‍♀️ AI Gym Trainer & Diet Advisor")

# Chatbot Section
st.header("💬 Diet Suggestion Bot")
goal = st.text_input("Your Goal (weight loss/muscle gain)")
preference = st.radio("Diet Preference", ['Veg', 'Non-Veg'])

if st.button("Get Diet Plan"):
    if goal:
        st.success(get_diet_recommendation(goal, preference))
    else:
        st.warning("Enter your goal!")

# Pose detection note
st.header("📹 Pose Detection")
st.write("Run `pose_detector.py` in terminal for live feedback using webcam.")

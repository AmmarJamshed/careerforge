import streamlit as st

from auth import login, signup
from chatbot import ai_chatbot
from booking import booking_page
from admin_dashboard import admin_dashboard
from ocr_tools import eligibility_engine

st.set_page_config(page_title="CareerForge", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

st.sidebar.title("CareerForge Platform")

menu = st.sidebar.selectbox(
    "Navigate",
    ["Login", "Signup", "Dashboard", "AI Chatbot", "OCR Eligibility Engine", "Counsellor Booking", "Admin"]
)

if menu == "Login":
    login()

elif menu == "Signup":
    signup()

elif menu == "Dashboard":
    if st.session_state["logged_in"]:
        st.title("🎓 Student Dashboard")
        st.write("Welcome", st.session_state["user"]["name"])
    else:
        st.error("Please login.")

elif menu == "AI Chatbot":
    ai_chatbot()

elif menu == "OCR Eligibility Engine":
    eligibility_engine()

elif menu == "Counsellor Booking":
    booking_page()

elif menu == "Admin":
    if st.session_state["logged_in"] and st.session_state["user"]["is_admin"] == 1:
        admin_dashboard()
    else:
        st.error("Admins only.")

import streamlit as st
from github_db import github_get, github_update

def booking_page():
    st.title("📅 Book a Counsellor Session")

    student = st.text_input("Your Name")
    counsellor = st.selectbox("Counsellor", ["Ammar Jamshed", "Empowerment Consultants"])
    date = st.date_input("Choose Date")
    time = st.time_input("Choose Time")

    if st.button("Book Session"):
        bookings, sha = github_get("bookings.json")

        bookings.append({
            "student": student,
            "counsellor": counsellor,
            "date": str(date),
            "time": str(time)
        })

        github_update("bookings.json", bookings, sha)

        st.success("Booking confirmed!")

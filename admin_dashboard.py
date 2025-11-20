import streamlit as st
from github_db import github_get

def admin_dashboard():
    st.title("🛠 Admin Dashboard")

    st.subheader("Users")
    users, _ = github_get("users.json")
    st.table(users)

    st.subheader("Bookings")
    bookings, _ = github_get("bookings.json")
    st.table(bookings)

    st.subheader("Consultants")
    consultants, _ = github_get("consultants.json")
    st.table(consultants)

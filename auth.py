import streamlit as st
from github_db import github_get, github_update

def signup():
    st.title("Create Account")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Signup"):
        users, sha = github_get("users.json")

        if any(u["email"] == email for u in users):
            st.error("Email already exists")
            return

        users.append({
            "name": name,
            "email": email,
            "password": password,
            "is_admin": 0
        })

        github_update("users.json", users, sha)

        st.success("Account created!")

def login():
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users, _ = github_get("users.json")

        user = next((u for u in users if u["email"] == email and u["password"] == password), None)

        if user:
            st.session_state["logged_in"] = True
            st.session_state["user"] = user
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials")

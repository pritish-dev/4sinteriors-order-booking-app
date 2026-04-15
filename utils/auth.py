import streamlit as st
from services.sheets import get_users

def login():
    st.title("🔐 Sales Login")

    users = get_users()

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        for u in users:
            if u["username"] == username and u["password"] == password:
                st.session_state["user"] = u
                st.success(f"Welcome {u['name']}")
                st.rerun()

        st.error("Invalid credentials")

def check_auth():
    return "user" in st.session_state
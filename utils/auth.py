import streamlit as st
from services.sheets import get_users

def clean(val):
    if val is None:
        return ""
    return str(val).strip()

def login():
    st.title("🔐 Sales Login")

    users = get_users()

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        input_user = clean(username)
        input_pass = clean(password)

        for u in users:
            sheet_user = clean(u.get("username"))
            sheet_pass = clean(u.get("password"))

            if sheet_user == input_user and sheet_pass == input_pass:
                st.session_state["user"] = u
                st.success(f"Welcome {u.get('name')}")
                st.rerun()

        st.error("Invalid credentials")

def check_auth():
    return "user" in st.session_state
import streamlit as st


def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    # Access credentials from secrets
    ADMIN_USERNAME = st.secrets["credentials"]["username"]
    ADMIN_PASSWORD = st.secrets["credentials"]["password"]

    if login_button:
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state["logged_in"] = True
            st.success("Successfully logged in!")
            st.rerun()
        else:
            st.error("Invalid username or password")
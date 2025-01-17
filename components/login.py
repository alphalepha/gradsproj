import streamlit as st


def login():
    """Simple login page."""
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if username == "admin" and password == "password":
            st.session_state["logged_in"] = True
        else:
            st.error("Invalid username or password")

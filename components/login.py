import streamlit as st


def login():
    st.markdown("Please login.")
    # username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    ADMIN_USERNAME = st.secrets["credentials"]["username"]
    ADMIN_PASSWORD = st.secrets["credentials"]["password"]

    if login_button:
        if password == ADMIN_PASSWORD:  # and username == ADMIN_USERNAME
            st.session_state["logged_in"] = True
            st.success("Successfully logged in!")
            st.rerun()
        else:
            st.error("Invalid username or password.")

import streamlit as st


def display_leaderboard(leaderboard_df):
    """Displays the leaderboard."""
    st.subheader("Updated Leaderboard")
    st.table(leaderboard_df.sort_values(by="Total Performance", ascending=False))

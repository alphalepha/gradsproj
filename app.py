import streamlit as st
from components.login import login
from components.leaderboard import display_leaderboard
from datetime import datetime
from components.stock_prices import plot_performance_with_emojis

st.set_page_config(page_title="Game Competition and Stock Tracker App",
                   layout="wide", )
# use wide layout
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

st.title("name")

start_date = '2025-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')
fig, leaderboard_df = plot_performance_with_emojis(start_date, end_date)
st.plotly_chart(fig)

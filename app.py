import streamlit as st
from components.login import login
from components.leaderboard import display_leaderboard
from components.stock_prices import get_stock_prices, dummy_weighting_function

st.set_page_config(page_title="Game Competition and Stock Tracker App",
                   layout="wide", )
# use wide layout
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
else:
    st.title("Game Competition and Stock Tracker App")
    if st.button("Refresh Leaderboard"):
        stock_prices_df = get_stock_prices()
        leaderboard_df = dummy_weighting_function(stock_prices_df)
        display_leaderboard(leaderboard_df)

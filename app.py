import streamlit as st
from components.login import login
from datetime import datetime
from components.utils import plot_performance_with_emojis, display_leaderboard

st.set_page_config(page_title="asdf", layout="wide", )

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()


st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Orbitron&display=swap" rel="stylesheet">
    <style>
    .highlight {
        background-color: #FF6600;  /* Orange background */
        color: #FFFFFF;  /* White text for contrast */
        padding: 0.1em 0.2em;  /* Adjust padding to reduce space */
        border-radius: 1px;
        display: inline-block; /* Prevent block-level spacing issues */
    }
    h3, h1 {
        margin: 0;  /* Remove default margin */
        padding: 0; /* Remove padding */
    }
    .stApp {
        font-family: 'Orbitron', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<span class='highlight'> Success depends upon previous preparation, and without such preparation, there is sure to be failure. </span> -- Confucius.", unsafe_allow_html=True)
st.divider()

start_date = st.secrets["dates"]["start_date"]
end_date = datetime.today().strftime('%Y-%m-%d')
players_data = st.secrets["players"]["players"]
player_emojis = st.secrets["player_emojis"]
fig, fig_stocks, leaderboard_df = plot_performance_with_emojis(players_data, start_date, end_date)

col1, col2 = st.columns([8, 2])
col1.markdown("<H3 style='margin: 0;'><span class='highlight'>Performance Chart (Chart will reset when game starts officially)</span></H3>", unsafe_allow_html=True)
col1.plotly_chart(fig)
col2.markdown("<H3 style='margin: 0;'><span class='highlight'>LEADERBOARD</span></H3>", unsafe_allow_html=True)
col2.dataframe(display_leaderboard(leaderboard_df), hide_index=True, use_container_width=True)

col2.divider()
if col2.button('reload_page'):
    st.rerun()

st.divider()
st.markdown("<H5 style='margin: 0;'><span class='highlight'>Individual Stocks</span></H3>", unsafe_allow_html=True)
st.plotly_chart(fig_stocks)

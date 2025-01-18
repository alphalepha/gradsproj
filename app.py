import streamlit as st
from components.login import login
from datetime import datetime
from components.stock_prices import plot_performance_with_emojis

st.set_page_config(page_title="asdf",
                   layout="wide", )
# use wide layout
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
        padding: 0.2em;
        border-radius: 4px;
    }
    .stApp {
        font-family: 'Orbitron', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<span class='highlight'>Success depends upon previous preparation, and without such preparation, there is sure to be failure.</span> -- Confucius.", unsafe_allow_html=True)

start_date = st.secrets["dates"]["start_date"]
end_date = datetime.today().strftime('%Y-%m-%d')
players_data = st.secrets["players"]["players"]
player_emojis = st.secrets["player_emojis"]
fig, leaderboard_df = plot_performance_with_emojis(players_data, player_emojis, start_date, end_date)
st.plotly_chart(fig)

st.divider()
if st.button('reload_page'):
    st.rerun()

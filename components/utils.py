import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
import json

import streamlit as st


def calculate_performance(players_data, start_date, end_date):
    players_portfolio = json.loads(players_data)

    performance_data = {}
    unique_stocks = set()

    for player in players_portfolio:
        unique_stocks.update(player['picks'])

    stock_data = yf.download(list(unique_stocks), start=start_date, end=end_date)['Close']
    if stock_data.empty or stock_data.dropna(how='all').empty:
        st.error('Error: Yahoo finance data is not available.')
        st.stop()

    stock_cumulative_returns = pd.DataFrame(index=stock_data.index, columns=stock_data.columns)

    stock_cumulative_returns.iloc[0, :] = 100
    stock_daily_returns = stock_data.pct_change(fill_method=None)
    stock_cumulative_returns.iloc[1:] = (1 + stock_daily_returns.iloc[1:]).cumprod() * 100

    ticker_to_name = {ticker: yf.Ticker(ticker).info.get("shortName", ticker) for ticker in stock_data.columns}
    stock_cumulative_returns.rename(columns=ticker_to_name, inplace=True)

    for player in players_portfolio:
        player_name = player['name']
        stocks = player['picks']

        player_stock_data = stock_data[stocks]

        player_cumulative_returns = pd.Series(index=player_stock_data.index, dtype=float)
        player_cumulative_returns.iloc[0] = 100

        player_daily_returns = player_stock_data.pct_change(fill_method=None).mean(axis=1)
        player_cumulative_returns.iloc[1:] = (1 + player_daily_returns.iloc[1:]).cumprod() * 100

        performance_data[player_name] = player_cumulative_returns

    players_performance_df = pd.DataFrame(performance_data).ffill()
    stock_performance_df = stock_cumulative_returns.ffill()

    return players_performance_df, stock_performance_df


def display_leaderboard(leaderboard_df):
    current_leaderboard = leaderboard_df.iloc[-1, :].copy()
    name = f"Stats as of: {current_leaderboard.name.strftime('%Y-%m-%d')}"
    current_leaderboard = current_leaderboard.reset_index()
    current_leaderboard.columns = ["Player", name]
    current_leaderboard[name] = current_leaderboard[name] - 100
    return current_leaderboard.sort_values(by=name, ascending=False).style.format({name: "{:.2f} %"})


def plot_performance_with_emojis(players_data, start_date, end_date):

    performance_df, stocks_performance_df = calculate_performance(players_data, start_date, end_date)

    fig = go.Figure()
    colors = [
        "#39ff14",
        "#7F00FF",
        "#00BFFF",
        "#1E90FF",
        "#FFD700",
        "#FF6347",
        "#00FFFF",
        "#002fa7"
    ]

    for i, player in enumerate(performance_df.columns):
        fig.add_trace(go.Scatter(x=performance_df.index, y=performance_df[player],
                                 mode='lines', name=player, line=dict(color=colors[i])))
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Performance",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    fig_stocks = go.Figure()
    for stock in stocks_performance_df.columns:
        fig_stocks.add_trace(
            go.Scatter(
                x=stocks_performance_df.index,
                y=stocks_performance_df[stock],
                mode='lines',
                name=stock
            )
        )
    fig_stocks.update_layout(
        xaxis_title="Date",
        yaxis_title="Cumulative Performance",
        legend_title="Stocks",
        template="plotly_dark",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig, fig_stocks, performance_df


def markdown():
    print('########## RERUN ##########')
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

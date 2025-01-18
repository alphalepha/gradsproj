import streamlit
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import json


# Function to calculate the performance of players based on their portfolio choices
def calculate_performance(start_date, end_date):
    # Hardcoded player information with stock portfolios
    players_data = st.secrets["players"]["players"]
    players_portfolio = json.loads(players_data)

    # This will store the performance data
    performance_data = {}

    for player in players_portfolio:
        player_name = player['name']
        stocks = player['picks']

        # Download the stock data for the given date range
        stock_data = yf.download(stocks, start=start_date, end=end_date)['Close']
        print(stock_data)
        # Calculate daily returns
        daily_returns = stock_data.pct_change().dropna()
        print(daily_returns)

        # Calculate equal-weighted portfolio return (average daily return of selected stocks)
        portfolio_returns = daily_returns.mean(axis=1)

        # Calculate the cumulative return from the start date to the end date
        # We start with 1 to ensure the portfolio starts at its initial value
        cumulative_returns = pd.Series(1, index=stock_data.index)
        cumulative_returns[1:] = (1 + portfolio_returns).cumprod()

        # Add the player's cumulative returns to the dictionary
        performance_data[player_name] = cumulative_returns

    # Convert the performance data to a DataFrame
    performance_df = pd.DataFrame(performance_data).ffill()

    # Return the DataFrame with player names as columns and performance over time
    return performance_df


# Function to plot the performance and include emojis based on player identity
def plot_performance_with_emojis(start_date, end_date):
    # Get the performance data
    performance_df = calculate_performance(start_date, end_date)

    # Create a Plotly figure
    fig = go.Figure()

    # Add performance trace for each player
    for player in performance_df.columns:
        fig.add_trace(go.Scatter(x=performance_df.index, y=performance_df[player], mode='lines', name=player))

    # Assign a unique emoji to each player
    player_emojis = {
        'DK': '🧑‍💼',
        'CF': '🧑‍🎤',
        'RZ': '🧑‍🏫',
        'VY': '🧑‍🏫',
        'TR': '🧑‍🏫',
        'PD': '🧑‍🏫',
        'MR': '🧑‍🏫',
        'MS': '🧑‍🏫',
    }

    # Add emojis and player names to represent each player's current performance at the latest date
    latest_date = performance_df.index[-1]

    for player in performance_df.columns:
        current_performance = performance_df[player].iloc[-1]
        emoji = player_emojis.get(player, '🙂')  # Default to a smiling emoji

        # Add the emoji and player name as a text annotation
        fig.add_annotation(
            x=latest_date,
            y=current_performance,
            text=f'{emoji} {player}',  # Add player name next to emoji
            showarrow=False,  # No arrow for this annotation
            font=dict(size=20),
            align='left',
            # Position the emoji at the end of the line, and player name slightly to the right
            xanchor='left',
            yanchor='middle',
            xshift=10  # Slightly shift the name to the right of the emoji
        )

    # Update layout
    fig.update_layout(
        title="Player Portfolio Performance",
        xaxis_title="Date",
        yaxis_title="Cumulative Return",
        showlegend=True
    )

    return fig, performance_df


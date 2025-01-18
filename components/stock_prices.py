import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import json


def calculate_performance(players_data, start_date, end_date):
    players_portfolio = json.loads(players_data)

    performance_data = {}

    for player in players_portfolio:
        player_name = player['name']
        stocks = player['picks']

        stock_data = yf.download(stocks, start=start_date, end=end_date)['Close']
        daily_returns = stock_data.pct_change().dropna()
        print(daily_returns)

        # Calculate equal-weighted portfolio return (average daily return of selected stocks)
        portfolio_returns = daily_returns.mean(axis=1)

        # Calculate the cumulative return from the start date to the end date
        # We start with 1 to ensure the portfolio starts at its initial value
        cumulative_returns = pd.Series(1.0, index=stock_data.index)
        cumulative_returns[1:] = (1 + portfolio_returns).cumprod()

        # Add the player's cumulative returns to the dictionary
        performance_data[player_name] = cumulative_returns

    # Convert the performance data to a DataFrame
    performance_df = pd.DataFrame(performance_data).ffill()

    # Return the DataFrame with player names as columns and performance over time
    return performance_df


# Function to plot the performance and include emojis based on player identity
def plot_performance_with_emojis(players_data, player_emojis, start_date, end_date):
    # Get the performance data
    performance_df = calculate_performance(players_data, start_date, end_date)

    # Create a Plotly figure
    fig = go.Figure()

    colors = [
        "#2E1A47",  # Dark Purple (cosmic nebula)
        "#7F00FF",  # Violet (space nebula glow)
        "#00BFFF",  # Deep Sky Blue (galaxy vibe)
        "#1E90FF",  # Dodger Blue (cosmic light)
        "#FFD700",  # Gold (stars and suns)
        "#FF6347",  # Tomato Red (fiery space objects)
        "#00FFFF",  # Cyan (futuristic space glow)
        "#4B0082"  # Indigo (space horizon)
    ]

    # Add performance trace for each player
    for i, player in enumerate(performance_df.columns):
        fig.add_trace(go.Scatter(x=performance_df.index, y=performance_df[player], mode='lines', name=player, line=dict(color=colors[i])))

    latest_date = performance_df.index[-1]

    for player in performance_df.columns:
        current_performance = performance_df[player].iloc[-1]
        emoji = player_emojis.get(player, '🙂')

        fig.add_annotation(
            x=latest_date,
            y=current_performance,
            text=f'{emoji} {player}',
            showarrow=False,
            font=dict(size=20),
            align='left',
            xanchor='left',
            yanchor='middle',
            xshift=10
        )

    # Update layout
    fig.update_layout(
        title="...",
        xaxis_title="Date",
        yaxis_title="Performance",
        showlegend=True
    )

    return fig, performance_df


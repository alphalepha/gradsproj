import plotly.graph_objects as go
import streamlit as st
import json
import pandas as pd
import yfinance as yf


def calculate_performance(players_data, start_date, end_date):
    players_portfolio = json.loads(players_data)

    start_date = pd.to_datetime(start_date).replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = pd.to_datetime(end_date).replace(hour=0, minute=0, second=0, microsecond=0)

    day_before_start_date = start_date - pd.Timedelta(days=1)

    performance_data = {}
    unique_stocks = set()

    for player in players_portfolio:
        unique_stocks.update(player['picks'])

    start_date_data = yf.download(list(unique_stocks), start=start_date, end=start_date + pd.Timedelta(days=1), interval="1d")
    if start_date_data.empty:
        return pd.DataFrame(), pd.DataFrame()

    opening_prices = start_date_data['Open'].iloc[0]
    closing_prices_start_date = start_date_data['Close'].iloc[0]
    opening_prices.name = start_date
    closing_prices_start_date.name = start_date

    historical_data = yf.download(list(unique_stocks), start=start_date + pd.Timedelta(days=1), end=end_date)['Close']
    if historical_data.empty or historical_data.dropna(how='all').empty:
        return pd.DataFrame(), pd.DataFrame()

    recent_data = yf.download(list(unique_stocks), period="1d")['Close']
    if not recent_data.empty:
        most_recent_prices = recent_data.iloc[-1]
        most_recent_prices.name = end_date
        historical_data = pd.concat([historical_data, pd.DataFrame([most_recent_prices])])
    else:
        return pd.DataFrame(), pd.DataFrame()

    combined_data = pd.concat([
        pd.DataFrame([opening_prices]),
        pd.DataFrame([closing_prices_start_date]),
        historical_data])

    stock_cumulative_returns = pd.DataFrame(index=[day_before_start_date] + list(combined_data.index[1:]), columns=combined_data.columns)

    stock_cumulative_returns.iloc[0, :] = 100
    stock_daily_returns = combined_data.pct_change(fill_method=None)
    stock_cumulative_returns.iloc[1:, :] = (1 + stock_daily_returns.iloc[1:, :]).cumprod() * 100

    ticker_to_name = {ticker: yf.Ticker(ticker).info.get("longName", ticker) for ticker in combined_data.columns}
    stock_cumulative_returns.rename(columns=ticker_to_name, inplace=True)

    for player in players_portfolio:
        player_name = player['name']
        stocks = player['picks']

        player_stock_data = combined_data[stocks]

        player_cumulative_returns = pd.Series(index=stock_cumulative_returns.index, dtype=float)
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

    if performance_df.empty or stocks_performance_df.empty:
        # Create empty Plotly figures
        fig = go.Figure()
        fig_stocks = go.Figure()

        # Return empty figures and an empty DataFrame
        return fig, fig_stocks, pd.DataFrame()

    fig = go.Figure()
    colors = [
        "#FF4500",  # Vibrant Orange-Red
        "#9400D3",  # Deep Violet
        "#1E90FF",  # Dodger Blue
        "#00FA9A",  # Medium Spring Green
        "#FFA500",
        "#FF69B4",  # Hot Pink
        "#40E0D0",  # Turquoise
        "#00008B",  # Dark Blue (strong contrast)
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


def styling():
    print('########## RERUN ##########')
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Orbitron&display=swap" rel="stylesheet">
        <style>
        .highlight {
            background-color: #007BFF;  /* Orange background */
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


def custom_divider(color="black", thickness="1px", margin="10px 0"):
    st.markdown(
        f"""
            <hr style="
                border: none;
                border-top: {thickness} solid {color};
                margin: {margin};
            ">
            """,
        unsafe_allow_html=True
    )

@st.cache_data
def map_stock_codes_to_names(stock_codes):
    """
    Map stock codes to their full names using yfinance.
    """
    stock_info = {}
    for code in stock_codes:
        try:
            stock = yf.Ticker(code)
            stock_info[code] = stock.info.get('longName', code)
        except Exception as e:
            stock_info[code] = code  # Fallback to code if info is not available
    return stock_info


@st.cache_data
def create_player_stock_table(players_json):
    # Parse the JSON string
    players = json.loads(players_json)

    # Extract all stock codes
    all_stock_codes = {code for player in players for code in player['picks']}

    # Map stock codes to real names using yfinance
    all_stocks = map_stock_codes_to_names(all_stock_codes)

    # Create an empty DataFrame with stocks as index and players as columns
    table = pd.DataFrame(index=all_stocks.values(), columns=[player['name'] for player in players])

    # Populate the table with 'x' where a player has the stock
    for player in players:
        for pick in player['picks']:
            real_name = all_stocks.get(pick, pick)
            table.loc[real_name, player['name']] = 'x'

    # Replace NaN with empty string
    table = table.fillna('')

    return table.transpose()


@st.cache_data
def get_stock_description(stock_code):
    """
    Fetch a short company description for a provided stock code using yfinance.
    """
    try:
        stock = yf.Ticker(stock_code)
        description = stock.info.get('longBusinessSummary', "Description not available")
        return description
    except Exception as e:
        return "Error retrieving description: " + str(e)


@st.cache_data
def get_unique_stock_list(players_json):
    """
    Extract a list of unique stock codes from the players JSON string.
    """
    players = json.loads(players_json)
    unique_stocks = sorted({code for player in players for code in player['picks']})
    return unique_stocks

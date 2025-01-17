import pandas as pd
import yfinance as yf


def get_stock_prices():
    """Fetches the current stock prices for a hardcoded list of tickers."""
    tickers = ["AAPL", "TSLA"]
    data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.history(period="1d")
        if not info.empty:
            current_price = info['Close'].iloc[-1]
            data.append({"Ticker": ticker, "Current Price": current_price})
        else:
            data.append({"Ticker": ticker, "Current Price": None})
    df = pd.DataFrame(data)
    df.set_index("Ticker", inplace=True)
    return df


def dummy_weighting_function(stock_prices_df):
    """Dummy function to calculate a leaderboard-like DataFrame based on stock prices."""
    data = {
        "Name": ["Alice", "Bob"],
        "Total Performance": [stock_prices_df["Current Price"].iloc[0] * 1.5, stock_prices_df["Current Price"].iloc[1] * 1.2],
        "Specific Performance 1": [stock_prices_df["Current Price"].iloc[0] * 0.5, stock_prices_df["Current Price"].iloc[1] * 0.4],
        "Specific Performance 2": [stock_prices_df["Current Price"].iloc[0] * 0.7, stock_prices_df["Current Price"].iloc[1] * 0.6],
        "Specific Performance 3": [stock_prices_df["Current Price"].iloc[0] * 0.3, stock_prices_df["Current Price"].iloc[1] * 0.2],
    }
    return pd.DataFrame(data)

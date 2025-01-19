import yfinance as yf

tickers = ["ETM.AX", "XTP.F", "11L.F", "TSLA", "AMZN", "POOL", "NVO", "NUE", "ADBE", "IXD1.F", "UNH", "DAR", "NVDA", "EL", "META", "RACE", "RHM.DE", "QBTS"]

for ticker in tickers:
    try:
        data = yf.download(ticker, period="1d")
        if data.empty:
            print(f"No data for {ticker}")
        else:
            print(f"Data found for {ticker}")
    except Exception as e:
        print(f"Error with {ticker}: {e}")

# test code to test yfinance dowload

import yfinance as yf
import streamlit as st
from datetime import datetime
import pandas as pd

unique_stocks = ['IXD1.F', 'RQ0.F', 'FB2A.F', 'NVD.F', 'TL0.F', 'SP1.F', 'NOV.F', 'G7PA.F', '2FE.F', 'RHM.F', 'AMZ.F', '11L.F', 'ELAA.F', 'XTP.F', 'ADB.F', 'NUO.F', 'DAR.F', 'UNH.F']
start_date = st.secrets["dates"]["start_date"]
end_date = (datetime.today()).strftime('%Y-%m-%d')

start_date = pd.to_datetime(start_date).replace(hour=0, minute=0, second=0, microsecond=0)
end_date = pd.to_datetime(end_date).replace(hour=0, minute=0, second=0, microsecond=0)
start_date_data = yf.download(list(unique_stocks), start=start_date, end=start_date + pd.Timedelta(days=1), interval="1d")
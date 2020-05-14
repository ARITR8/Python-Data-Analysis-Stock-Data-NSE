import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_finance import volume_overlay3

plt.style.use('ggplot')

import numpy as np
from datetime import datetime
import ta
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpl_dates
from sqlalchemy import create_engine
from ta.volatility import BollingerBands
from ta.trend import MACD
from ta.trend import ema_indicator
from ta.momentum import StochasticOscillator
from ta.volume import on_balance_volume
from ta.trend import ADXIndicator
from sqlalchemy import create_engine

plt.style.use('ggplot')
# Loading of data from postgres table
table_name = 'historical_data'
dbname = 'Stock'
host = 'localhost'
user = 'postgres'
pwd = 'password'
port = '5432'
SYMBOL = "'20MICRONS                     '"

conn = f'postgres://{user}:{pwd}@{host}:{port}/{dbname}'
print(conn)
engine = create_engine(conn)

date_recorded = "date_recorded"
series = "series"
prev_close_price = "prev_close_price"
open_price = "open_price"
high_price = "high_price"
low_price = "low_price"
last_price = "trim(last_price:: text)"
close_price = "close_price"
vwap = "vwap"
volume = "volume"
turnover = "turnover"
trades = "trades"
deliverable_volume = "deliverable_volume"
prcntg_deliverble = "prcntg_deliverble"
bb_bbm = "trim(bb_bbm:: text)"

df = pd.read_sql_query(f'select {low_price}  low_price, {open_price} open_price,'
                       f'{close_price} close_price , {date_recorded} date_recorded ,'
                       f'{high_price} high_price , {volume} volume'
                       f' from historical_data where historical_data.symbol  = {SYMBOL}', conn)

low = df["low_price"].to_list()
print(low)
high = df["high_price"]
print(high)
close = df["close_price"]
print(close)
print(df.columns)

"""For MACD"""

indicator = MACD(close=df["close_price"], n_slow=26, n_fast=12, n_sign=9, fillna=False)

print(indicator)
df['MACD'] = indicator.macd()
df['MACD_SIGNAL'] = indicator.macd_signal()
print(df)

"""For Relative Strength: Stochastics (14,7,3)"""

indicator = StochasticOscillator(close=df["close_price"], high=df["high_price"], low=df["low_price"], n=14, d_n=3,
                                 fillna=False)

print(indicator)
df['STOCH'] = indicator.stoch()
df['STOCH_SIGNAL'] = indicator.stoch_signal()
print(df)

print(df.columns)

indicator = ADXIndicator(high=df["high_price"], low=df["low_price"], close=df["close_price"], n=14, fillna=True)
print(indicator)
df['ADX_NEG'] = indicator.adx_neg()
df['ADX_POSVT_indicator'] = indicator.adx_pos()
df['ADX_indicator'] = indicator.adx()
# df['ADX'] = indicator.adx()
print(df)

print(df)
"""OBV"""
indicator = on_balance_volume(close=df["close_price"], volume=df["volume"], fillna=True)
print(indicator)
df['obv_indicator'] = indicator
print(df)

"""EMA"""

indicator = ema_indicator(close=df["close_price"], n=12, fillna=True)
print(indicator)
df['EMA_indicator'] = indicator
print(df)

df.to_sql('technical_analysis',engine)

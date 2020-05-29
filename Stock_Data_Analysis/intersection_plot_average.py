import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
from sqlalchemy import create_engine
import io
import sys
import psycopg2
from mpl_finance import volume_overlay3
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates

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
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
import datetime
import numpy as np

import matplotlib.pyplot as plt


import os

execution_path = os.getcwd()

plt.style.use('ggplot')
# Loading of data from postgres table
table_name = 'historical_data'
dbname = 'Stock'
host = 'localhost'
user = 'postgres'
pwd = 'password'
port = '5432'
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
volume1 = "volume1"
turnover = "turnover"
trades = "trades"
deliverable_volume = "deliverable_volume"
prcntg_deliverble = "prcntg_deliverble"
bb_bbm = "trim(bb_bbm:: text)"
macd_signal = "macd_signal_indicator"
macd = "macd_indicator"

table_name = 'historical_data'
df1 = pd.read_sql(table_name,conn)
df_unique_symbols = (df1 ['symbol'].unique())
m = 0
df2 = pd.DataFrame()
SYMBOL = "'20MICRONS                     '"

    #print(SYMBOL)
df = pd.read_sql_query(f'select {low_price}  low_price, {open_price} open_price,{macd} MACD,{macd_signal} MACD_SIGNAL,'
                       f'{close_price} close_price , {date_recorded} date_recorded ,'
                       f'{high_price} high_price , {volume1} volume , {SYMBOL} symbol'
                       f' from technical_analysis where technical_analysis.symbol  = {SYMBOL}', conn)

low = df["low_price"].to_list()
# print(low)
high = df["high_price"]
# print(high)
close = df["close_price"]
plt.figure()

x = df['date_recorded']
y1 = df['macd']
y2 = df['macd_signal']
# Set the labesls for the axes
fig = plt.figure(figsize=(16,18))
gs = gridspec.GridSpec(2,1, height_ratios=[5,1])
# Set tight layout to minimize gaps between subplots
plt.tight_layout()
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1], sharex=ax1)
ax2.xaxis_date()

dates = df.index.tolist()
#dates = ['11-2019', '12-2019', '01-2020']
#dates = [datetime.strptime(x, '%m-%Y') for x in dates]
# Convert the date to the mdates format
N = 100
#dates = pd.DataFrame(mdates.date2num(dates), columns=['date_recorded'])
#dates = pd.date_range(start='2015-03-01', periods=N, freq='D')
#dates=pd.DataFrame(np.random.rand(84,3),index=[chr(ascii) for ascii in range(33,33+84)])
start_date = '2019-12-12'
end_date = '2020-05-15'
# Set x and y axis limits

#ax1.set_ylim([minPrice, maxPrice])

# Set the labesls for the axes
#ax1.set_ylabel('Price($)', fontsize = 16)

xlabels = ax2.get_xticklabels()
ax2.set_xticklabels(xlabels, rotation = 45, fontsize = 12)



# Change the x-axis tick label format
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))




y1.plot(color = 'g', style = ['-'], linewidth = 2.5, ax = ax2)
y2.plot(color = 'b', style = ['-'], linewidth = 2.5, ax = ax2)
#diff.plot(color = 'black', style = ['-'], linewidth = 2.0, ax = ax2)
#plt.show()
plt.plot(x, y1, '-')
plt.plot(x, y2, '-')

idx = np.argwhere(np.diff(np.sign(y1- y2))).flatten()
plt.plot(x[idx], y1[idx], 'ro')
plt.show()
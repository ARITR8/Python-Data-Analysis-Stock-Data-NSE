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
from ta.trend import  ADXIndicator
plt.style.use('ggplot')
# Loading of data from postgres table
table_name = 'historical_data'
dbname = 'Stock'
host = 'localhost'
user = 'postgres'
pwd = 'password'
port = '5432'
SYMBOL = "'TATAMOTORS                     '"

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
                       f' from historical_data where historical_data.symbol  = {SYMBOL}',conn )


#df = ta.add_all_ta_features(df, open = "open_price" , high = "high_price" , low = "low_price" , close = "close_price" ,
 #                           volume= "volume", fillna= True)
low = df["low_price"].to_list()
print(low)
high = df["high_price"]
print (high)
close = df["close_price"]
print(close)
#print(df["low_price"])
print(df.columns)
indicator = ADXIndicator( high= df["high_price"], low = df["low_price"] , close = df["close_price"], n=14, fillna= True)
print(indicator)
df['ADX_NEG'] = indicator.adx_neg()
df['ADX_POSVT'] = indicator.adx_pos()
#df['RSI']=indicator.rsi()
df['ADX'] = indicator.adx()
print(df)




ohlc = df.loc[:, ['date_recorded', 'open_price', 'high_price', 'low_price', 'close_price']]
#print(ohlc)

#Now got the price of the tatamotors

#aapl['Date'] = aapl.index.map(mdates.date2num)

ohlc['date_recorded'] = pd.to_datetime(ohlc['date_recorded'])
ohlc['date_recorded'] = ohlc['date_recorded'].apply(mpl_dates.date2num)
#ohlc = ohlc.astype(float)


# Creating Subplots
fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(14,7), num='candle chart')



#candlestick_ohlc(ax[0], ohlc.values, width=0.4, colorup='green', colordown='red', alpha=0.5)


# Setting labels & titles

idx = df[date_recorded]

df['index'] = idx


candlestick_ohlc(ax[0], ohlc.values, width=0.4, colorup='green', colordown='red', alpha=0.5)


# Setting labels & titles
ax[0].set_xlabel('Date')
ax[0].set_ylabel('Price')
fig.suptitle(f'Daily Candlestick Chart of {SYMBOL}')



ax[1].plot(df.date_recorded, df.ADX_POSVT)
ax[1].plot(df.date_recorded, df.ADX_NEG)
#ax[1].plot(df.date_recorded, df.ADX)

#adding volume overlay

#ax2 = ax[1].twinx()

#bc = plt.volume_overlay (ax2 , df["open_price"])


xfmt = mpl.dates.DateFormatter('%d-%m-%Y')

#ax[1].xaxis.set_major_locator(mpl.dates.DayLocator(interval=5))
ax[1].xaxis.set_major_formatter(xfmt)

#ax[1].xaxis.set_minor_locator(mpl.dates.DateLocator(interval=3))
ax[1].xaxis.set_minor_formatter(xfmt)

ax[1].get_xaxis().set_tick_params(which='major', pad=25)

fig.autofmt_xdate()
plt
plt.show()
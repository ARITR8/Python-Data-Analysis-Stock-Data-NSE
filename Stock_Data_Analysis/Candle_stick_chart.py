import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpl_dates
from sqlalchemy import create_engine

plt.style.use('ggplot')
# Loading of data from postgres table
table_name = 'historical_data'
dbname = 'Stock'
host = 'localhost'
user = 'postgres'
pwd = 'password'
port = '5432'
SYMBOL = "'TATAMOTORS'"

conn = f'postgres://{user}:{pwd}@{host}:{port}/{dbname}'
print(conn)
engine = create_engine(conn)

df = pd.read_sql_query(f'select * from historical_data where historical_data.symbol  = {SYMBOL}',conn)
print(df)
ohlc = df.loc[:, ['date_recorded', 'open_price', 'high_price', 'low_price', 'close_price']]
#print(ohlc)

#Now got the price of the tatamotors

#aapl['Date'] = aapl.index.map(mdates.date2num)

ohlc['date_recorded'] = pd.to_datetime(ohlc['date_recorded'])
ohlc['date_recorded'] = ohlc['date_recorded'].apply(mpl_dates.date2num)
#ohlc = ohlc.astype(float)


# Creating Subplots
fig, ax = plt.subplots(figsize=(14,7), num='candle chart')

candlestick_ohlc(ax, ohlc.values, width=0.4, colorup='green', colordown='red', alpha=0.5)


# Setting labels & titles
ax.set_xlabel('Date')
ax.set_ylabel('Price')
fig.suptitle(f'Daily Candlestick Chart of {SYMBOL}')

# Formatting Date
date_format = mpl_dates.DateFormatter('%d-%m-%Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate()

#fig.tight_layout()

plt.show()










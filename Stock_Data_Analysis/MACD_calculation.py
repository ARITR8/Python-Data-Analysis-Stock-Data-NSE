#%matplotlib inline
import matplotlib.pyplot as plt
#from pandas import rolling_mean
plt.style.use('ggplot')

import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine

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
volume = "volume"
turnover = "turnover"
trades = "trades"
deliverable_volume = "deliverable_volume"
prcntg_deliverble = "prcntg_deliverble"
bb_bbm = "trim(bb_bbm:: text)"

table_name = 'historical_data'
df1 = pd.read_sql(table_name,conn)
df_unique_symbols = (df1 ['symbol'].unique())
m = 0
df2 = pd.DataFrame()

SYMBOL = "'ALPSINDUS                     '"

df = pd.read_sql_query(f'select {low_price}  low_price, {open_price} open_price,'
                       f'{close_price} close_price , {date_recorded} date_recorded ,'
                       f'{high_price} high_price , {volume} volume , {SYMBOL} symbol'
                       f' from historical_data where historical_data.symbol  = {SYMBOL}', conn)


print (df)
#df = pd.DataFrame(web.DataReader(stock, 'google', start, end)['Close'])
df = df.reset_index()
print(df["close_price"])
#df['30 mavg'] = pd.rolling_mean(df["close_price"], 30)

df_moving_average = df.close_price.rolling(30).mean()
print(df_moving_average)
df_moving_average_26 = df.close_price.rolling(26).mean()
print(df_moving_average_26)
df_moving_average_12 = df.close_price.rolling(12).mean()
print(df_moving_average_12)
df_macd = (df_moving_average_12 - df_moving_average_26)
print(df_macd)






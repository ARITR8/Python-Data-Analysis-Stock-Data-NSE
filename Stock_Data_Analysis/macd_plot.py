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

from ta.trend import MACD
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
SYMBOL = "'BPCL                     '"
df2 = pd.DataFrame()
for i in df_unique_symbols:
    #SYMBOL = "'ALPSINDUS                     '"

    #print(SYMBOL)
    SYMBOL = f'\'{i}\''




    #print(SYMBOL)
    df = pd.read_sql_query(f'select {low_price}  low_price, {open_price} open_price,{macd} MACD,{macd_signal} MACD_SIGNAL,'
                       f'{close_price} close_price , {date_recorded} date_recorded ,'
                       f'{high_price} high_price , {volume1} volume , {SYMBOL} symbol'
                       f' from technical_analysis where technical_analysis.symbol  = {SYMBOL}', conn)



    print(df)

    try:
        df['Signal Line Crossover'] = np.where(df['macd'] > df['macd_signal'], 1, 0)
        print(df)
        df['Signal Line Crossover'] = np.where(df['macd'] < df['macd_signal'], -1, df['Signal Line Crossover'])
        print(df)
        df['Buy Sell signal line'] = (2*(np.sign(df['Signal Line Crossover'] - df['Signal Line Crossover'].shift(1))))
        print(df)

        df['Centerline Crossover'] = np.where(df['macd'] > 0, 1, 0)
        df['Centerline Crossover'] = np.where(df['macd'] < 0, -1, df['Centerline Crossover'])
    except TypeError  as e:
        df['Signal Line Crossover'] = 111
        df['Signal Line Crossover'] = 111
        df['Buy Sell signal line'] = 111
        df['Centerline Crossover'] =111
        df['Centerline Crossover'] =111

    """For MACD"""

    indicator = MACD(close=df["close_price"], n_slow=26, n_fast=12, n_sign=9, fillna=False)

    MACD_INDICATOR = "MACD_indicator"

    # print(indicator)
    df[MACD_INDICATOR] = indicator.macd()
    df["MACD_SIGNAL_indicator"] = indicator.macd_signal()
    df2 = df2.append(df)
    df2.to_csv('MACD_price_buy_sell.csv', mode='w', header=False)
    m=m+1


def pg_load_table(file_path, table_name1, dbname, host, port, user, pwd):
    '''
    This function upload csv to a target table
        '''
    try:
        conn = psycopg2.connect(dbname=dbname, host=host, port=port,
                                user=user, password=pwd)
        print("Connecting to Database")
        cur = conn.cursor()
        f = open(file_path, "r")
        # Truncate the table first
        # cur.execute("Truncate {} Cascade;".format(table_name))
        # print("Truncated {}".format(table_name))
        # Load table from the file with header
        cur.copy_expert("copy {} from STDIN CSV HEADER QUOTE '\"'".format(table_name1), f)  # f is removed from here
        cur.execute("commit;")
        print("Loaded data into {}".format(table_name1))
        conn.close()
        print("DB connection closed.")

    except Exception as e:
        print("Error: {}".format(str(e)))
        sys.exit(1)

table_name = 'buy_sell_signal_all'

file_path = 'F:\Python-Stock_Analysis\Stock_Data_Analysis\MACD_price_buy_sell.csv'
dbname = 'Stock'
host = 'localhost'
user = 'postgres'
pwd = 'password'
port = '5432'

pg_load_table(file_path, table_name, dbname, host, port, user, pwd)

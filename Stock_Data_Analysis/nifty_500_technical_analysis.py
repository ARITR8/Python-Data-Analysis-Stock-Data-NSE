import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
from sqlalchemy import create_engine
import io
import sys
import psycopg2
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

table_name = 'nity_500_historical_data'
df1 = pd.read_sql(table_name,conn)
df_unique_symbols = (df1 ['symbol'].unique())
m = 0
df2 = pd.DataFrame()
for i in df_unique_symbols:
    #SYMBOL = "'ALPSINDUS                     '"

    #print(SYMBOL)
    SYMBOL = f'\'{i}\''

    print(SYMBOL)

    df = pd.read_sql_query(f'select {low_price}  low_price, {open_price} open_price,'
                       f'{close_price} close_price , {date_recorded} date_recorded ,'
                       f'{high_price} high_price , {volume} volume , {SYMBOL} symbol'
                       f' from nity_500_historical_data where nity_500_historical_data.symbol  = {SYMBOL}', conn)

    low = df["low_price"].to_list()
    #print(low)
    high = df["high_price"]
    #print(high)
    close = df["close_price"]
    #print(close)
    #print(df.columns)

    """For MACD"""

    indicator = MACD(close=df["close_price"], n_slow=26, n_fast=12, n_sign=9, fillna=False)

    MACD_INDICATOR = "MACD_indicator"


   # print(indicator)
    df[MACD_INDICATOR] = indicator.macd()
    df["MACD_SIGNAL_indicator"] = indicator.macd_signal()

   # print(df)

    """For Relative Strength: Stochastics (14,7,3)"""

    indicator = StochasticOscillator(close=df["close_price"], high=df["high_price"], low=df["low_price"], n=14, d_n=3,
                                 fillna=False)

    #print(indicator)
    df["STOCH_indicator"] = indicator.stoch()
    df["STOCH_SIGNAL_indicator"] = indicator.stoch_signal()
    #print(df)

    #print(df.columns)

    try:
        indicator = ADXIndicator(high=df["high_price"], low=df["low_price"], close=df["close_price"], n=14, fillna=True)
        #print(indicator)
        df["ADX_NEG_indicator"] = indicator.adx_neg()
        df["ADX_POSVT_indicator"] = indicator.adx_pos()
        try:
            df["ADX_indicator"] = indicator.adx()
        except (IndexError,ValueError) as e:
            df["ADX_indicator"] = "0"
            print("The ADX error is coming for SYMBOL" + f'{i}')
    except (IndexError, ValueError) as e:
        df["ADX_indicator"] = "0"
        print("The ADX error is coming for SYMBOL" + f'{i}')
    # df['ADX'] = indicator.adx()
    #print(df)

    #print(df)
    """OBV"""
    indicator = on_balance_volume(close=df["close_price"], volume=df["volume"], fillna=True)
    #print(indicator)
    df["obv_indicator"] = indicator
    #print(df)

    """EMA"""

    indicator = ema_indicator(close=df["close_price"], n=12, fillna=True)
    #print(indicator)
    df["EMA_indicator"] = indicator
    #print(df)
    df2 = df2.append(df)
    df2.to_csv('nifty_500_MACD_price.csv', mode='w', header=False)


table_name1 = 'nifty_500_technical_analysis'





def pg_load_table(file_path, table_name1, dbname, host, port, user, pwd):
    '''
    This function upload csv to a target table
        '''
    try:
        conn = psycopg2.connect(dbname=dbname, host=host, port = port,
                                    user=user, password=pwd)
        print("Connecting to Database")
        cur = conn.cursor()
        f = open(file_path, "r")
        # Truncate the table first
        cur.execute("Truncate {} Cascade;".format(table_name1))
        print("Truncated {}".format(table_name1))
        # Load table from the file with header
        cur.copy_expert("copy {} from STDIN CSV HEADER QUOTE '\"'".format(table_name1), f )#f is removed from here
        cur.execute("commit;")
        print("Loaded data into {}".format(table_name1))
        conn.close()
        print("DB connection closed.")

    except Exception as e:
        print("Error: {}".format(str(e)))
        sys.exit(1)
file_path = 'F:\Python-Stock_Analysis\Stock_Data_Analysis\\nifty_500_MACD_price.csv'
dbname = 'Stock'
host = 'localhost'
user = 'postgres'
pwd = 'password'
port = '5432'
pg_load_table(file_path, table_name1, dbname, host, port, user, pwd)

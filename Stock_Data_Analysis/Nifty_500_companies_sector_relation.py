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
#table_name = 'historical_data'
dbname = 'Stock'
host = 'localhost'
user = 'postgres'
pwd = 'password'
port = '5432'

conn = f'postgres://{user}:{pwd}@{host}:{port}/{dbname}'
print(conn)
engine = create_engine(conn)


table_name1 = 'NIFTY_INDICES_SYMBOL_RELATION'
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


file_path = 'F:\Python-Stock_Analysis\Stock_Data_Analysis\ind_nifty500list.csv'
dbname = 'Stock'
host = 'localhost'
user = 'postgres'
pwd = 'password'
port = '5432'
pg_load_table(file_path, table_name1, dbname, host, port, user, pwd)
#MACD_price_buy_sell.csv
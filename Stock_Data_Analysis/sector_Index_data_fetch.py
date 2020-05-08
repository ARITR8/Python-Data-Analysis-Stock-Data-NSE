import inspect
import pandas as pd
import sqlalchemy
import csv
from sqlalchemy import create_engine
import io
import sys
import psycopg2
from nsepy import get_history
from datetime import date
from nsepy.urls import *
import six
from nsepy.commons import *
from nsepy.constants import *
from datetime import date, timedelta
from bs4 import BeautifulSoup
import pandas as pd
import six
import inspect
import io
import pdb
import pandas_datareader as web
from pandas.util.testing import assert_frame_equal
import cx_Oracle


class sector_indices_fetch:
    def __init__(self, file_name):
        """

        This Class will generate historical price data of various Nifty indexes
          and will populate it in the postgres database
        """
        self.fileName = file_name

    def stock_symbol_store(self):
        raw_data = pd.read_csv(self.fileName)
        raw_list = list(raw_data.Symbol)
        raw_list.pop(0)
        print(raw_list)
        return raw_list


    def load_data_csv(self, arr, start_date, end_date):
        df2 = pd.DataFrame()
        df3 = pd.DataFrame()

        for i in arr:
            #data_output = get_history(symbol=i, start=start_date, end=end_date)
            #print(i)
            data_output = get_history(symbol=i,
                                       start=start_date,
                                       end=end_date,
                                       index=True)

            print(data_output)
            #print(df_list)
            df2 = df2.append(data_output) ###--- for one value

            df_list = []
            for item in df2.iterrows()  :
                df_list.append(i)
                #print (df_list)
            print(df_list)

            print(type(df_list))
            df2['indices'] = df_list

            print(df2)

            df2 = df2.append(df2)
            df2.to_csv('historical_price_indices.csv', mode='w', header=False)


    def pg_load_table(self, file_path, table_name, dbname, host, port, user, pwd):
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
            cur.execute("Truncate {} Cascade;".format(table_name))
            print("Truncated {}".format(table_name))
            # Load table from the file with header
            cur.copy_expert("copy {} from STDIN CSV HEADER QUOTE '\"'".format(table_name), f)
            cur.execute("commit;")
            print("Loaded data into {}".format(table_name))
            conn.close()
            print("DB connection closed.")

        except Exception as e:
            print("Error: {}".format(str(e)))
            sys.exit(1)


obj1 = sector_indices_fetch("Nifty_indices.csv")
k1 = obj1.stock_symbol_store()
obj1.load_data_csv(k1, date(2020, 1, 1), date(2020, 5, 7))
# obj1.load_data_oracle()
file_path = 'F:\Python-Stock_Analysis\Stock_Data_Analysis\historical_price_indices.csv'
table_name = 'historical_data_indices'
dbname = 'Stock'
host = 'localhost'
user = 'postgres'
pwd = 'password'
port = '5432'
#obj1.pg_load_table(file_path, table_name, dbname, host, port, user, pwd)

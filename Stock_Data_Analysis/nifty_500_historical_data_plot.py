import pandas as pd
import sqlalchemy
import csv
from sqlalchemy import create_engine
import io
import sys
import psycopg2
from nsepy import get_history
from datetime import date
import pandas_datareader as web
from pandas.util.testing import assert_frame_equal
import cx_Oracle

class PriceData:
    def __init__(self, file_name):
        """

        This Class will generate historical price data and will populate it in the postgres database
        """
        self.fileName = file_name

    def stock_symbol_store(self):
        raw_data = pd.read_csv(self.fileName)
        raw_list = list(raw_data.Symbol)
        #raw_list.pop(0)
        # print(raw_list)
        return raw_list

    def load_data_csv(self, arr, start_date, end_date):
        df2 = pd.DataFrame()
        for i in arr:
            print(i)
            data_output = get_history(symbol=i, start=start_date, end=end_date)
            print(data_output)
            df2 = df2.append(data_output)
            df2.to_csv('nifty_500_historical_price.csv', mode='w', header=False)


    def pg_load_table(self,file_path, table_name, dbname, host, port, user, pwd):
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
            cur.execute("Truncate {} Cascade;".format(table_name))
            print("Truncated {}".format(table_name))
            # Load table from the file with header
            cur.copy_expert("copy {} from STDIN CSV HEADER QUOTE '\"'".format(table_name), f )#f is removed from here
            cur.execute("commit;")
            print("Loaded data into {}".format(table_name))
            conn.close()
            print("DB connection closed.")

        except Exception as e:
            print("Error: {}".format(str(e)))
            sys.exit(1)

    def load_data_oracle(self):
         reader = csv.reader(open("data.csv", "r"))
         lines = []
         for line in reader:
             lines.append(line)
         con = cx_Oracle.connect('system/password@localhost/XE')
         ver = con.version.split(".")
         print(ver)
         cur = con.cursor()
         for kine in lines:
             cur.execute(" INSERT INTO historical_data ('date_recorded', 'symbol','series', 'prev_close_price',  'open_price',"
                         "'high_price' ,'low_price' ,'last_price' ,"
                         " 'close_price', 'vwap' , 'volume' ,   'turnover' ,   "
                         " 'trades' ,                'deliverable_volume',                'prcntg_deliverble' ) VALUES(:1,:2,:3,:4,:5,:6, :7, :8 , :9, :10, :11, :12, :13, :14, :15)" ,
                 kine)
         con.commit()
         cur.close()


#arr = ['TATAMOTORS','M&M','MRF','MOTHERSUMI','APOLLOTYRE','AMARAJABAT','BAJAJ-AUTO','HEROMOTOCO','TVSMOTOR','MARUTI','BHARATFORG','BOSCHLTD']
obj1 = PriceData("ind_nifty100list.csv")
k1 = obj1.stock_symbol_store()
print(k1)
print(len(k1))

#obj1.load_data_csv(arr, date(2020, 4, 11), date(2020, 5, 11))

obj1.load_data_csv(k1, date(2020, 1, 1), date(2020, 7, 30))

#obj1.load_data_oracle()
file_path = 'F:\Python-Stock_Analysis\Stock_Data_Analysis\\nifty_500_historical_price.csv'
table_name = 'nity_500_historical_data'
dbname = 'Stock'
host = 'localhost'
user = 'postgres'
pwd = 'password'
port = '5432'
obj1.pg_load_table(file_path, table_name, dbname, host, port, user, pwd)
import datetime
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import AutoDateFormatter, AutoDateLocator

class BarChartPlot():
    def __init__(self, table_name , dbname, host, user, pwd, port  ):
        self.table_name = table_name
        self.dbname = dbname
        self.host = host
        self.user= user
        self.pwd = pwd
        self.port = port

    def db_fetch_query(self, my_query):
        conn = f'postgres://{user}:{pwd}@{host}:{port}/{dbname}'
        engine = create_engine(conn)
        df = pd.read_sql_query(my_query, conn)
        return df
    def bar_chart_plot(self,df):
        k1 = df['price_change'].to_list()
        df['dummy_col'] = df['price_change'] > 0
        k2 = df['symbol'].to_list()
        k3 = k1
        print(k3)
        #DateStrList = ['01/01/2010', '02/01/2010']
        k1= df.dummy_col.map( {True: 'g'})
        print(df)
        fig,ax = plt.subplots()
        ax = df['price_change'].plot(kind='bar',
                             color=df.dummy_col.map({True: 'g', False: 'r'}))

        start_date = df['start_date'].to_list()
        start_date = start_date[0]
        end_date = df['end_date'].to_list()
        end_date = end_date[0]
        ax.set_title(f'chart generated starting from {start_date} to {end_date}')

        print(type(ax))
        rects = ax.patches
        plt.minorticks_on()
        plt.grid(which='major', linestyle='-', linewidth='0.5', color='red')
        # Customize the minor grid
        plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
        ax.set_ylabel("PRICE", fontsize=12)
        ax.set_xticklabels(k2, rotation=1)
        i = 0
        #ax.set_xticklabels(k3..strftime('%Y-%m'))
        #fig, ax1 = plt.subplot
        for rects in  ax.patches:

            height = rects.get_height()
            width = rects.get_width()
            x = rects.get_x()
            y = rects.get_y()
            label_x = x + width - 0.2
            label_y = (y + height) + 0.87
            print("width "+ str(width))
            print(height)
            plt.text( label_x , label_y , height , ha="center", va="bottom", color="black",
                     fontsize=7, fontweight="bold" )
            i=i+1;

        plt.show()







table_name = 'historical_data_indices'
dbname = 'Stock'
host = 'localhost'
user = 'postgres'
pwd = 'password'
port = '5432'

#6month plotting
mysql_6 = '''SELECT trim(M1.SYMBOL) SYMBOL, M1.OPEN_PRICE  , M2.CLOSE_PRICE , (M2.CLOSE_PRICE-M1.OPEN_PRICE) PRICE_CHANGE
FROM HISTORICAL_DATA_INDICES M1 , HISTORICAL_DATA_INDICES M2
WHERE M1.DATE_RECORDED = '2019-11-29'
AND M2.DATE_RECORDED = '2020-05-07'
AND M1.SYMBOL = M2.SYMBOL'''

#3month plotting
mysql_3 = '''SELECT trim(M1.SYMBOL) SYMBOL, M1.OPEN_PRICE  , M2.CLOSE_PRICE , (M2.CLOSE_PRICE-M1.OPEN_PRICE) PRICE_CHANGE
FROM HISTORICAL_DATA_INDICES M1 , HISTORICAL_DATA_INDICES M2
WHERE M1.DATE_RECORDED = '2020-02-01'
AND M2.DATE_RECORDED = '2020-05-07'
AND M1.SYMBOL = M2.SYMBOL'''

mysql_31 = '''SELECT trim(M1.SYMBOL) SYMBOL,
 M1.OPEN_PRICE  ,
  M2.CLOSE_PRICE ,
   (M2.CLOSE_PRICE-M1.OPEN_PRICE) PRICE_CHANGE  , m1.date_recorded as start_date , m2.date_recorded as end_date
FROM HISTORICAL_DATA_INDICES M1 , HISTORICAL_DATA_INDICES M2
WHERE M1.DATE_RECORDED = '2019-11-29'
AND M2.DATE_RECORDED = '2020-02-01'
AND M1.SYMBOL = M2.SYMBOL'''

#one month old data
mysql_1 = '''SELECT trim(M1.SYMBOL) SYMBOL, M1.OPEN_PRICE  , M2.CLOSE_PRICE , (M2.CLOSE_PRICE-M1.OPEN_PRICE) PRICE_CHANGE
FROM HISTORICAL_DATA_INDICES M1 , HISTORICAL_DATA_INDICES M2
WHERE M1.DATE_RECORDED = '2020-04-01'
AND M2.DATE_RECORDED = '2020-05-06'
AND M1.SYMBOL = M2.SYMBOL'''


#1 week old data
mysql_1w = '''SELECT trim(M1.SYMBOL) SYMBOL, M1.OPEN_PRICE  , M2.CLOSE_PRICE , (M2.CLOSE_PRICE-M1.OPEN_PRICE) PRICE_CHANGE
FROM HISTORICAL_DATA_INDICES M1 , HISTORICAL_DATA_INDICES M2
WHERE M1.DATE_RECORDED = '2020-04-24'
AND M2.DATE_RECORDED = '2020-05-06'
AND M1.SYMBOL = M2.SYMBOL'''


obj1 = BarChartPlot(table_name, dbname, host, user, pwd, port)
df = obj1.db_fetch_query(mysql_31)
obj1.bar_chart_plot(df)



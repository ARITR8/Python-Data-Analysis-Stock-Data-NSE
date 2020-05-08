import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
import datetime
import matplotlib.pyplot as plt
import openpyxl
from openpyxl import Workbook
from openpyxl.drawing.image import Image


table_name = 'historical_data_indices'
dbname = 'Stock'
host = 'localhost'
user = 'postgres'
pwd = 'password'
port = '5432'

conn = f'postgres://{user}:{pwd}@{host}:{port}/{dbname}'
print(conn)
engine = create_engine(conn)

#for i in

mysql = '''SELECT trim(M1.SYMBOL) SYMBOL, M1.OPEN_PRICE  , M2.CLOSE_PRICE , (M2.CLOSE_PRICE-M1.OPEN_PRICE) PRICE_CHANGE
FROM HISTORICAL_DATA_INDICES M1 , HISTORICAL_DATA_INDICES M2
WHERE M1.DATE_RECORDED = '2019-11-29'
AND M2.DATE_RECORDED = '2020-05-07'
AND M1.SYMBOL = M2.SYMBOL'''

df = pd.read_sql_query(mysql, conn)

#print(df)
print(df['price_change'].to_list())
k1 = df['price_change'].to_list()
df['dummy_col'] = df['price_change'] > 0
#print(k1)
k2 = df['symbol'].to_list()
print(k2)
k1= df.dummy_col.map( {True: 'g'})

ax = df['price_change'].plot(kind='bar',
                             color=df.dummy_col.map({True: 'g', False: 'r'}))

ax.set_title("Sector performance analysis for 6 months old data")

rects = ax.patches
plt.minorticks_on()
plt.grid(which='major', linestyle='-', linewidth='0.5', color='red')
# Customize the minor grid
plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')



#ax = df[['price_change']].plot(kind = 'barh',
#color = df.dummy_col.map({True : 'g', False: 'r'}) )
for lp in k2:
    m1 = lp
    print(m1)
#ax.set_xlabel(k2, fontsize=12)
#ax.xaxis_date()     # interpret the x-axis values as dates
#fig.autofmt_xdate() # make space for and rotate the x-axis tick labels

ax.set_ylabel("PRICE", fontsize=12)
label1 = (label12 for label12 in k2)

print(label1)
#label = "{:.1f}".format(label1)
#print(label)

ax.set_xticklabels(k2, rotation=1)
plt.show()








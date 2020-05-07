import pandas as pd
from sqlalchemy import create_engine
import datetime
import matplotlib.pyplot as plt
import openpyxl
from openpyxl import Workbook
from openpyxl.drawing.image import Image


table_name = 'historical_data'
dbname = 'Stock'
host = 'localhost'
user = 'postgres'
pwd = 'password'
port = '5432'

conn = f'postgres://{user}:{pwd}@{host}:{port}/{dbname}'
print(conn)
engine = create_engine(conn)

df = pd.read_sql(table_name,conn)
#create each separate data frames based on symbols
df_unique_symbols = (df ['symbol'].unique())


#print two columns
#print(df.loc[0],['close_price', 'date_recorded'])

xfile = openpyxl.load_workbook('Book 4.xlsx')
page=xfile.active
#sheet = xfile.get_sheet_by_name('Sheet1')
for i in df_unique_symbols:

    #exec("sticky"+str(i)+"  = df[df.symbol == i]")
    k1 = "v"+str(i)
    k1 = df[df.symbol == i]
    print(k1)
    #k1.head()
    k1.set_index('date_recorded', inplace=True)
    #k1.truncate(before='2020-02-22')['Close'].plot(figsize=(16, 12))
    k1['close_price'].plot(label = f'{k1}', figsize = (16,8), title = f'closing price of {i}')
    #plt.legend()
    plt.show()
    #namepng = f'{i}'
    #namepng=namepng.strip()
    #print(namepng)
    #plt.savefig('namepng.png')
    #image = Image('namepng.png')
    #page.append(image)
    #sheet.add_image(image, 'L6')
xfile.save('Book 4.xlsx')

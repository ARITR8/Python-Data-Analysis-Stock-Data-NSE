import pandas as pd
import sqlalchemy
from nsepy import get_history
from datetime import date
import pandas_datareader as web


class PriceData:
    def __init__(self, file_name):
        """

        This Class will generate historical price data and will populate it in the postgres database
        """
        self.fileName = file_name

    def stock_symbol_store(self):
        raw_data = pd.read_csv(self.fileName)
        raw_list = list(raw_data.Symbol)
        raw_list.pop(0)
        # print(raw_list)
        return raw_list

    def get_historical_data(self, arr, start_date, end_date, output_file):
        for i in arr:
            data_output = get_history(symbol=i, start=start_date, end=end_date)
            pd.to_csv(data_output)


obj1 = PriceData("data.csv")
k1= obj1.stock_symbol_store()
obj1.get_historical_data(k1, date(2020, 4, 29), date(2020, 4, 30), "output.csv")

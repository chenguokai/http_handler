from sys import flags
from DataCleanHelper import DataCleanHelper
from DataQueryHelper import DataQueryHelper
import pandas as pd
import json

class Wrapper:
    def __init__(self,user) -> None:
        self.clean_helper_wechat = DataCleanHelper(True)
        self.clean_helper_alipay = DataCleanHelper(False)
        df1 = self.clean_helper_wechat.PreProcess(user)
        df2 = self.clean_helper_alipay.PreProcess(user)
        self.csv_file = self.concate(df1,df2)

        self.query_helper = DataQueryHelper()

    def concate(self,df1,df2):
        if df1.empty and df2.empty:
            return df1
        elif df1.empty:
            return df2
        elif df2.empty:
            return df1
        else:
            return pd.concat([df1,df2], axis=0) 

    def get_monthly_income(self,year,month):
        res = {}
        res["res"] = self.query_helper.get_monthly_income(self.csv_file,year,month)
        return json.dumps(res)
    
    def get_monthly_outcome(self,year,month):
        res = {}
        res["res"] = self.query_helper.get_monthly_outcome(self.csv_file,year,month)
        return json.dumps(res)

    def get_year_income(self,year):
        return json.dumps(self.query_helper.get_year_income(self.csv_file,year))
    
    def get_year_outcome(self,year):
        return json.dumps(self.query_helper.get_year_outcome(self.csv_file,year))

    def sort_by_cost(self,type,ISoutcome=True):
        res = {}
        res["res"] = self.query_helper.sort_by_cost(self.csv_file,type,ISoutcome)
        return json.dumps(res)

    def sort_by_frequency(self,type,ISoutcome=True):
        return json.dumps(self.query_helper.sort_by_frequency(self.csv_file,type,ISoutcome))

    def query_all(self,type):
        res = {}
        res["state"] = False if self.csv_file.empty else True
        res["result"] = self.query_helper.sort_by_cost(self.csv_file,type,True)

        return json.dumps(res)

    def get_outcome(self):
        return json.dumps(self.query_helper.get_outcome(self.csv_file))

    def get_income(self):
        return json.dumps(self.query_helper.get_income(self.csv_file))
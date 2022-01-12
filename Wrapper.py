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

        self.query_helper = DataQueryHelper(user)

    def concate(self,df1,df2):
        if df1.empty and df2.empty:
            return df1
        elif df1.empty:
            return df2
        elif df2.empty:
            return df1
        else:
            return pd.concat([df1,df2], axis=0) 

    def query_all(self,type):
        res = {}
        res["state"] = False if self.csv_file.empty else True
        res["result"] = self.query_helper.sort_by_cost(self.csv_file,type,ISoutcome=True)

        return json.dumps(res)

    def get_outcome(self):
        return json.dumps(self.query_helper.get_income_or_outcome(self.csv_file,ISoutcome=True))

    def get_income(self):
        return json.dumps(self.query_helper.get_income_or_outcome(self.csv_file,ISoutcome=False))
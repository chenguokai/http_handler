from DataCleanHelper import DataCleanHelper
from DataQueryHelper import DataQueryHelper
import json

class Wrapper:
    def __init__(self,user) -> None:
        self.clean_helper = DataCleanHelper()
        self.query_helper = DataQueryHelper()
        self.csv_file = self.clean_helper.PreProcess(user)

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

    def query_all(self,type,year):
        res = {}
        res["month"] = self.query_helper.query_valid_year(self.csv_file,year)
        res["res"] = self.query_helper.sort_by_cost(self.csv_file,type,True)

        return json.dumps(res)
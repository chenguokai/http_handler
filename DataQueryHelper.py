import numpy as np
from BillHelper import BillHelper
from Config import config

class DataQueryHelper:
    def __init__(self, user):
        self.bill_helper = BillHelper(user)

    def __select_date(self,df, year_start=2021, month_start=1, day_start=1, year_end=2021, month_end=12, day_end=31):
        date_start = year_start*10**10+month_start*10**8+day_start*10**6
        date_end = year_end*10**10+month_end*10**8+(day_end+1)*10**6
        res = df[(date_start <= df["交易时间"]) & (df["交易时间"] < date_end)]
        return res

    def __get_income(self,df):
        return df[df["收/支"] == '收入']["金额"].sum()

    def __get_outcome(self,df):
        return df[df["收/支"] == '支出']["金额"].sum()

    def get_monthly_income(self,df,year,month):
        data = self.__select_date(df,year_start=year,year_end=year,month_start=month,month_end=month)
        if config.disable_database:
            return round(self.__get_income(data),2)
        else:
            income = self.__get_income(data)
            self.bill_helper.insert_bill_table(year, month, income, True)
            return round(self.bill_helper.select_bill_table(year, month, True), 2)

    def get_monthly_outcome(self,df,year,month):
        data = self.__select_date(df,year_start=year,year_end=year,month_start=month,month_end=month)
        if config.disable_database:
            return round(self.__get_outcome(data),2)
        else:
            outcome = self.__get_outcome(data)
            self.bill_helper.insert_bill_table(year, month, outcome, False)
            return round(self.bill_helper.select_bill_table(year, month, False), 2)

    def get_year_income(self,df,year):
        '''
        format 
        [
            '1' : 10,
            '2' : 1000,
            ...
            '12' : 1000
        ]
        '''
        result = []
        for i in range(12):
            result.append(self.get_monthly_income(df,year,i+1))
        return result


    def get_year_outcome(self,df,year):
        '''
        format
        [
            '1' : 10,
            '2' : 1000,
            ...
            '12' : 1000
        ]
        '''
        result = []
        for i in range(12):
            result.append(self.get_monthly_outcome(df,year,i+1))
        return result

    def sort_by_cost(self,df,type,ISoutcome=True):
        '''
        type:'交易对方' or '类型' or ...
        ISoutcome: True -> 根据支出分类 ; False -> 根据收入分类
        '''
        result = []
        data = df.groupby(type)
        for key,value in data:
            item = {}
            if ISoutcome:
                money = self.__get_outcome(value)
            else:
                money = self.__get_income(value)

            if money != 0.0:
                if(config.disable_database):
                    item["category"] = key
                    item["amount"] = round(money, 2)
                    item["repeat"] = float(value[value["收/支"] == '支出']["金额"].count())
                else:
                    print(key)
                    count = float(value[value["收/支"] == '支出']["金额"].count())
                    self.bill_helper.insert_category(key, money, count)
                    [money, count] = self.bill_helper.select_category(key)
                    item["category"] = key
                    item["amount"] = round(money, 2)
                    item["repeat"] = count
                result.append(item)
        return sorted(result, key=lambda item:item["amount"], reverse=True)

    def sort_by_frequency(self,df,type,ISoutcome=True):
        '''
        type:'交易对方' or '类型' or ...
        ISoutcome: True -> 根据支出分类 ; False -> 根据收入分类
        '''
        result = {}
        keys = df['交易对方'].value_counts().keys()
        values = df['交易对方'].value_counts()

        for key in keys:
            result[key] = float(values[key])
        return sorted(result.items(), key=lambda item:item[1], reverse=True)

    def query_valid_year(self,df,year):
        tmp = self.get_year_outcome(df,year)
        res = []
        for i in range(12):
            if tmp[(i + 1)] != 0:
                res.append((i + 1))
        return res

    def get_income(self,df):
        res = {}
        res["state"] = False if df.empty else True

        if df.empty:
            res["result"] = {}
            return res
        
        year_start = self.get_start_year(df)
        year_end = self.get_end_year(df)

        tmp = []

        for year in range(year_start,year_end + 1):
            year_info = self.get_year_income(df,year)
            for (month,income) in enumerate(year_info):
                tmp_res = {}
                if income != 0:
                    tmp_res["month"] = "%s.%s" % (year,(("%s" % (month + 1)).zfill(2)) )
                    tmp_res["money"] = income
                    tmp.append(tmp_res)

        res["result"] = tmp
        return res
                
            

    def get_outcome(self,df):
        res = {}
        res["state"] = False if df.empty else True

        if df.empty:
            res["result"] = {}
            return res
        
        year_start = self.get_start_year(df)
        year_end = self.get_end_year(df)

        tmp = []

        for year in range(year_start,year_end + 1):
            year_info = self.get_year_outcome(df,year)
            for (month,outcome) in enumerate(year_info):
                tmp_res = {}
                if outcome != 0:
                    tmp_res["month"] = "%s.%s" % (year,(("%s" % (month + 1)).zfill(2)) )
                    tmp_res["money"] = outcome
                    tmp.append(tmp_res)

        res["result"] = tmp
        return res

    def get_start_year(self,df):
        return int(df["交易时间"].min() / 10**10)

    def get_end_year(self,df):
        return int(df["交易时间"].max() / 10**10)

        
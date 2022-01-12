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

    def __get_income_or_outcome(self,df,ISoutcome=True):
        if ISoutcome:
            return df[df["收/支"] == '支出']["金额"].sum()
        else:
            return df[df["收/支"] == '收入']["金额"].sum()

    def __get_monthly_income_or_outcome(self,df,year,month,ISoutcome=True):
        data = self.__select_date(df,year_start=year,year_end=year,month_start=month,month_end=month)
        if config.disable_database:
            return round(self.__get_income_or_outcome(data,ISoutcome),2)
        else:
            result = self.__get_income_or_outcome(data,ISoutcome)
            self.bill_helper.insert_bill_table(year, month, result, True)
            return round(self.bill_helper.select_bill_table(year, month, True), 2)

    def __get_year_income_or_outcome(self,df,year,ISoutcome=True):
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
            result.append(self.__get_monthly_income_or_outcome(df,year,i+1,ISoutcome))
        return result

    def __get_start_year(self,df):
        return int(df["交易时间"].min() / 10**10)

    def __get_end_year(self,df):
        return int(df["交易时间"].max() / 10**10)

    def sort_by_cost(self,df,type,ISoutcome=True):
        '''
        type:'交易对方' or '类型' or ...
        ISoutcome: True -> 根据支出分类 ; False -> 根据收入分类
        '''
        result = []
        data = df.groupby(type)
        for key,value in data:
            item = {}
            money = self.__get_income_or_outcome(value,ISoutcome)

            if money != 0.0:
                if(config.disable_database):
                    item["category"] = key
                    item["amount"] = round(money, 2)
                    if ISoutcome:
                        item["repeat"] = float(value[value["收/支"] == '支出']["金额"].count())
                    else:
                        item["repeat"] = float(value[value["收/支"] == '收入']["金额"].count())
                else:
                    print(key)
                    if ISoutcome:
                        count = float(value[value["收/支"] == '支出']["金额"].count())
                    else:
                        count = float(value[value["收/支"] == '收入']["金额"].count())
                    self.bill_helper.insert_category(key, money, count)
                    [money, count] = self.bill_helper.select_category(key)
                    item["category"] = key
                    item["amount"] = round(money, 2)
                    item["repeat"] = count
                result.append(item)
        return sorted(result, key=lambda item:item["amount"], reverse=True)

    def get_income_or_outcome(self,df,ISoutcome=True):
        res = {}
        res["state"] = False if df.empty else True

        if df.empty:
            res["result"] = {}
            return res
        
        year_start = self.__get_start_year(df)
        year_end = self.__get_end_year(df)

        tmp = []

        for year in range(year_start,year_end + 1):
            year_info = self.__get_year_income_or_outcome(df,year,ISoutcome)
            for (month,money) in enumerate(year_info):
                tmp_res = {}
                if money != 0:
                    tmp_res["month"] = "%s.%s" % (year,(("%s" % (month + 1)).zfill(2)) )
                    tmp_res["money"] = money
                    tmp.append(tmp_res)

        res["result"] = tmp
        return res
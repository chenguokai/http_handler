import pandas as pd
import os
import time
from Config import config

class DataCleanHelper:

    def __init__(self,isWechat) -> None:
        self.isWechat = isWechat
        self.__encoding = config.encoding_wechat if isWechat else config.encoding_alipay
        self.__focus = config.focus

    def is_wechat(self,file):
        '''
        判断是否是微信文件
        是 -> 微信支付账单明细列表 所在行号
        否 -> -1
        '''
        with open(file,"r",encoding=self.__encoding) as f:
            lines = f.readlines()
        start_line = 0;
        for line in lines:
            start_line += 1
            if "微信支付账单明细列表" in line:
                return start_line
        return -1

    def data_clean(self,csv_file):

        if("金额(元)" in csv_file.columns):
            csv_file.rename(columns={"金额(元)":"金额"},inplace=True)
        if("金额（元）   " in csv_file.columns):
            csv_file.rename(columns={"金额（元）   ":"金额"},inplace=True)
        if("收/支     " in csv_file.columns):
            csv_file.rename(columns={"收/支     ":"收/支"},inplace=True)
        if('类型              ' in csv_file.columns):
            csv_file.rename(columns={'类型              ':"类型"},inplace=True)
        if('交易对方            ' in csv_file.columns):
            csv_file.rename(columns={'交易对方            ':"交易对方"},inplace=True)
        
        if(self.isWechat):
            csv_file["金额"] = csv_file["金额"].str.replace("¥","");

        csv_file["收/支"] = csv_file["收/支"].str.replace("      ",""); 
        csv_file["金额"] = csv_file["金额"].apply(lambda i: float(i));

        if("交易创建时间" in csv_file.columns):
            csv_file.rename(columns={"交易创建时间":"交易时间"},inplace=True)

        if("交易创建时间              " in csv_file.columns):
            csv_file.rename(columns={"交易创建时间              ":"交易时间"},inplace=True)

        if("交易类型" in csv_file.columns):
            csv_file.rename(columns={"交易类型":"类型"},inplace=True)
        

        csv_file["交易时间"] = csv_file["交易时间"].str.replace("-","");
        csv_file["交易时间"] = csv_file["交易时间"].str.replace(" ","");
        csv_file["交易时间"] = csv_file["交易时间"].str.replace(":","");
        csv_file["交易时间"] = csv_file["交易时间"].str.replace("/","");
        csv_file["交易时间"] = csv_file["交易时间"].apply(lambda i: int(i));

        if("交易单号" in csv_file.columns):
            csv_file["交易单号"] = csv_file["交易单号"].str.replace("\t","");

        if("商户单号" in csv_file.columns):
            csv_file["商户单号"] = csv_file["商户单号"].str.replace("\t","");

        if("类型" in csv_file.columns):
            csv_file["类型"] = csv_file["类型"].str.replace(" ","")

        if("交易对方" in csv_file.columns):
            csv_file["交易对方"] = csv_file["交易对方"].str.replace(" ","")
        
        #csv_file.columns = columns

        tmp_columns = csv_file.columns
        for column in tmp_columns:
            if column in self.__focus:
                continue
            else:
                del csv_file[column]

    
    def PreProcess(self,user):
        '''
        
        '''
        USER = user
        BASE = config.path
        prefix = "wechat" if self.isWechat else "alipay"
        FILE_RAW = os.path.join(BASE,USER,prefix,"data")
        DIR_RAW = os.listdir(FILE_RAW)
        FILE_CSV = os.path.join(BASE,USER,prefix,"clean")
        if not os.path.exists(FILE_CSV):
            os.mkdir(FILE_CSV)
        flag = -1

        # name of the columns
        # 交易号，商家订单号，交易创建时间，付款时间，最近修改时间，交易来源地 ，类型，交易对方  ，商品名称 ，金额（元），收/支  ，交易状态，服务费（元），成功退款（元），备注，资金状态 
        columns = self.__focus

        if len(DIR_RAW) == 0 :
            return pd.DataFrame(columns = self.__focus) #创建一个空的dataframe

        if len(DIR_RAW) != 1 :
            print("more than 1 file in raw directory")
            exit();

        target_file = os.path.join(FILE_CSV,DIR_RAW[0])
        raw_file = os.path.join(FILE_RAW,DIR_RAW[0])

        raw_file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(raw_file).st_mtime))

        if not os.path.exists(target_file) or raw_file_modify_time > time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(target_file).st_mtime)):
            # file do not exsit, create it 
            # or the raw file is newer than the target file
            with open(raw_file,"r",encoding=self.__encoding) as f1:
                list1 = f1.readlines()
            with open(target_file,"w",encoding=self.__encoding) as f2:
                flag = self.is_wechat(raw_file)
                if flag != -1:
                    for (index , line) in enumerate(list1):
                        if index >= flag:
                            f2.write(line)
                else:
                    for (index , line) in enumerate(list1):
                        if index > 3 and index < (len(list1) - 7):
                            f2.write(line)

        csv_file = pd.read_csv(target_file,encoding=self.__encoding)

        self.data_clean(csv_file)

        return csv_file

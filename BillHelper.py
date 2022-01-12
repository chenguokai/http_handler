import pymysql
from Config import config

class BillHelper:
    def __init__(self, user):
        self.user = user
        if(config.disable_database == False):
            self.create_bill_table(True)
            self.create_bill_table(False)
            self.delete_bill_table(True)
            self.delete_bill_table(False)
            self.create_category()
            self.delete_category()

    def get_db(self): 
        db = pymysql.connect(
            host = '127.0.0.1',	#mysql服务器地址
            port = 3306,		#端口号
            user = 'root',		#用户名
            passwd = '      ',	#密码
            db = 'bill',		#数据库名称
            charset="utf8",
        )
        return db

    def init_bill_table(self, is_income):
        db = self.get_db()
        cursor = db.cursor()
        if is_income:
            cursor.execute("DROP TABLE IF EXISTS INCOME")
        else:
            cursor.execute("DROP TABLE IF EXISTS OUTCOME")
        db.close()

    def create_bill_table(self, is_income):
        db = self.get_db()
        cursor = db.cursor()
        if is_income:
            sql = """CREATE TABLE IF NOT EXISTS INCOME (
                USER_NAME  CHAR(30) NOT NULL,
                YEAR INT,
                MONTH INT,  
                INCOME FLOAT,
                PRIMARY KEY (USER_NAME, YEAR, MONTH)) """
        else:
            sql = """CREATE TABLE IF NOT EXISTS OUTCOME (
                USER_NAME  CHAR(30) NOT NULL,
                YEAR INT,
                MONTH INT,  
                OUTCOME FLOAT,
                PRIMARY KEY (USER_NAME, YEAR, MONTH)) """
        cursor.execute(sql)
        db.close()

    def insert_bill_table(self, year, month, income, is_income):
        db = self.get_db()
        cursor = db.cursor()
        if(is_income):
            sql = "INSERT INTO INCOME(USER_NAME, \
                YEAR, MONTH, INCOME) VALUES (%s, %s, %s, %s) \
                ON DUPLICATE KEY UPDATE INCOME=INCOME+%s;"
        else:
            sql = "INSERT INTO OUTCOME(USER_NAME, \
                YEAR, MONTH, OUTCOME) VALUES (%s, %s, %s, %s) \
                ON DUPLICATE KEY UPDATE OUTCOME=OUTCOME+%s;"
        cursor.execute(sql, [self.user, year, month, income, income])
        db.commit()
        db.close()

    def delete_bill_table(self, is_income):
        db = self.get_db()
        cursor = db.cursor() 
        if is_income:
            sql = "DELETE FROM INCOME WHERE USER_NAME=%s;"
        else:
            sql = "DELETE FROM OUTCOME WHERE USER_NAME=%s;"
        cursor.execute(sql, self.user)
        db.commit()
        db.close()
        
    def select_bill_table(self, year, month, is_income):
        db = self.get_db()
        cursor = db.cursor()
        if is_income:
            sql = "SELECT * FROM INCOME \
            WHERE USER_NAME = %s \
            AND YEAR = %s \
            AND MONTH = %s;"
        else:
            sql = "SELECT * FROM OUTCOME \
            WHERE USER_NAME = %s \
            AND YEAR = %s \
            AND MONTH = %s;"
        cursor.execute(sql, [self.user, year, month])
        results = cursor.fetchall()
        for row in results:
            db.close()
            return row[3]

    def init_category_table(self):
        db = self.get_db()
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS COST")
        db.close()

    def create_category(self):
        db = self.get_db()
        cursor = db.cursor()
        sql = """CREATE TABLE IF NOT EXISTS COST (
                USER_NAME  CHAR(30) NOT NULL,
                CATEGORY  CHAR(30) NOT NULL, 
                COST FLOAT,
                COUNT FLOAT,
                PRIMARY KEY (USER_NAME, CATEGORY)) """
        cursor.execute(sql)
        db.close()
    
    def insert_category(self, category, cost, count):
        db = self.get_db()
        cursor = db.cursor()
        sql = "INSERT INTO COST(USER_NAME, \
                CATEGORY, COST, COUNT) VALUES (%s, %s, %s, %s) \
                ON DUPLICATE KEY UPDATE COST=COST+%s, COUNT=COUNT+%s;"
        cursor.execute(sql, [self.user, category, cost, count, cost, count])
        db.commit()
        db.close()

    def delete_category(self):
        db = self.get_db()
        cursor = db.cursor()
        sql = "DELETE FROM COST WHERE USER_NAME=%s;"
        cursor.execute(sql, self.user)
        db.commit()
        db.close()

    def select_category(self, category):
        db = self.get_db()
        cursor = db.cursor()
        sql = "SELECT * FROM COST \
            WHERE USER_NAME = %s \
            AND CATEGORY = %s;"
        cursor.execute(sql, [self.user, category])
        results = cursor.fetchall()
        for row in results:
            cost = row[2]
            count = row[3]
            db.close()
            return [cost, count]
  
# billhelper = BillHelper()  
# billhelper.init_bill_table(True)
# billhelper.init_bill_table(False)
# billhelper.create_bill_table(True)
# billhelper.insert_bill_table('user1', 2021, 10, 2000, True)
# billhelper.select_bill_table('user1', 2021, 10, True)
# billhelper.create_bill_table(False)
# billhelper.insert_bill_table('user1', 2021, 9, 4000, False)
# billhelper.select_bill_table('user1', 2021, 9, False)
#delete_bill_table('user1', True)
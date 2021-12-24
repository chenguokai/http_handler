
import pymysql
import dbconfig as conf
import logging
import sys


# database controller class
class DBController:

    def __init__(self):
        self.logger = logging.getLogger("baseSpider")
        self.formatter = logging.Formatter('%(asctime)s\
                    %(levelname)-8s:%(message)s')
        self.file_handler = logging.FileHandler("user-database.log")
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        self.logger.setLevel(logging.INFO)
        self.conn = None
        self.cursor = None

    def db_connect(self):
        #print(conf.db_config)
        try:
            self.conn = pymysql.connect(host=conf.db_config['host'], port=conf.db_config['port'], user=conf.db_config['user'], password=conf.db_config['password'],
                                    db=conf.db_config['db'], charset = conf.db_config['charset'])
        except:
            self.logger.error("Database connection failed!")
            return False
        self.cursor = self.conn.cursor()
        return True

    def db_close(self):
        if self.conn and self.cursor:
            self.cursor.close()
            self.conn.close()
        return True

    def db_execute(self, sql):
        #print(sql)
        status = self.db_connect()
        if status == False:
            return False
        try:
            if self.conn and self.cursor:
                self.cursor.execute(sql)
                self.conn.commit()
        except:
            self.logger.error("sql execution failed: " + sql)
            self.db_close()
            return False
        result = self.cursor.fetchall()
        self.db_close()
        return result

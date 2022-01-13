
import hashlib
import dbutil
import uuid
import http.client
import json
import os

class UserModule:

    def __init__(self):
        self.db = dbutil.DBController()
        self.return_format = {
            'result'    :   '',
            'reason'    :   '',
            'token'     :   ''
        }

    def construct_return(self, resultval, reasonstr, tokenstr):
        self.return_format['result'] = resultval
        self.return_format['reason'] = reasonstr
        self.return_format['token'] = tokenstr
        return self.return_format

    def finduser(self, name):
        sql = "select * from users where name = \'" + name + "\'"
        result = self.db.db_execute(sql)
        if result == False:
            return False
        return result

    def register(self, name, password):
        find_result = self.finduser(name)
        if find_result == False:
            return json.dumps(self.construct_return(False, "database error", ''))
        if find_result:
            return json.dumps(self.construct_return(False, "user has been registered", ''))
        md5pw = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
        sql = "insert into users(name, password) values(\'" + name + "\', \'" + md5pw + "\')"
        result = self.db.db_execute(sql)
        if result == False:
            return json.dumps(self.construct_return(False, "database error", ''))
        else:
            # test TBD
            # structure like this:
            # .
            # └── 0001
            #     ├── alipay
            #     │   ├── data
            #     │   └── upload.php
            #     └── wechat
            #         ├── data
            #         └── upload.php

            base = "/var/www/html"
            php_path = os.path.join(base,"upload.php")
            user_path = os.path.join(base,"data",name)
            wechat_user_path = os.path.join(user_path,"wechat")
            alipay_user_path = os.path.join(user_path,"alipay")
            if not os.path.exists(user_path):
                os.makedirs(user_path)
            if not os.path.exists(wechat_user_path):
                os.makedirs(wechat_user_path)
            if not os.path.exists(alipay_user_path):
                os.makedirs(alipay_user_path)

            os.mkdir(os.path.join(wechat_user_path,"data"))
            os.mkdir(os.path.join(alipay_user_path,"data"))

            os.system("cp %s %s" % (php_path,wechat_user_path))
            os.system("cp %s %s" % (php_path,alipay_user_path))

            os.chmod(user_path,777)
            
            return json.dumps(self.construct_return(True, "registration succeeded", ''))

    def login(self, name, password):
        find_result = self.finduser(name)
        if find_result == False:
            return json.dumps(self.construct_return(False, "database error", ''))
        if find_result == ():
            return json.dumps(self.construct_return(False, "wrong username or password", ''))
        md5pw = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
        if md5pw == find_result[0][1]:
            uuidstr = str(uuid.uuid4())
            return json.dumps(self.construct_return(True, "login succeeded", uuidstr))
        else:
            return json.dumps(self.construct_return(False, "wrong username or password", ''))

    def delete(self, name):
        sql = "delete from users where name = \'" + name + "\'"
        result = self.db.db_execute(sql)
        if result == False:
            return json.dumps(self.construct_return(False, "database error", ''))
        else:
            return json.dumps(self.construct_return(True, "delete succeeded", ''))

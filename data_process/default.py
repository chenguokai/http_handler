import usermodule as um
import Wrapper

class default():
    def handle_request(self, request_uuid, method):
        if method == "sort":
            tmp = Wrapper.Wrapper(request_uuid)
            return tmp.query_all("交易对方")
        elif method == "monthOutcome":
            tmp = Wrapper.Wrapper(request_uuid)
            return tmp.get_outcome()
        elif method == "monthIncome":
            tmp = Wrapper.Wrapper(request_uuid)
            return tmp.get_income()

            
            return "a valid data processing value\n"
    def handle_register(self, request_uuid, request_token, method):
        user = um.UserModule()
        if method == "register":
            result = user.register(request_uuid, request_token)
            return result
        elif method == "login":
            result = user.login(request_uuid, request_token)
            return result


class default():
    def handle_request(self, request_uuid, method):
        if method == "j_call":
            return "a valid data processing value\n"
    def handle_register(self, request_uuid, request_token, method):
        if method == "register" or method == "login":
            return "a valid data processing value\n"

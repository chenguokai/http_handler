class default():
    def handle_request(self, request_uuid, method):
        if request_uuid == "0000" and method == "j_call":
            return "a valid data processing value\n"
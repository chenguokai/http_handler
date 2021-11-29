class default():
    def handle_request(self, request_uuid, method):
        if method == "j_call":
            return "a valid data processing value\n"
from data_process.default import default

class Controller:
    def __init__(self):
        self._request = ""
        self._reply = ""
        self._filename = ""
        self._token = ""
        self._uuid = ""
        self.post_method = "append"
        self.code_not_found = "HTTP/1.1 404 Not Found\r\n"
        self.code_ok = "HTTP/1.1 200 OK\r\n"
        self.server_info = "Server: My server\r\n\r\n"
        self.reply_no_service = "Have got your request but we do not provide user-readable service"
        self.reply_cannot_understand = "Cannot understand"
        self.reply_received = "Map Received"
        self.request_invalid = "You are sending an invalid request"
        self.backend_invalid = "Invalid return value from backend"
        self.uuid_token_dic = {"0000": "2333"}
        self.invalid_input = "invalid"

    def web_params(self, filename, token, uuid):
        self._filename = filename
        self._token = token
        self._uuid = uuid

    def add_to_database(self, uuid, token):
        self.uuid_token_dic[uuid] = token
    def find(self, uuid):
        if uuid in self.uuid_token_dic:
            return self.uuid_token_dic[uuid]
        else:
            return None

class webController(Controller):
    @property
    def reply(self):
        return self._reply

    def handle_post(self):
        print("handle post: ", self._uuid, self._token)
        if self._uuid is None or self._token is None:
            return self.code_not_found + self.server_info + self.request_invalid
        self.add_to_database(self._uuid, self._token)
        return self.code_ok + self.server_info + self.reply_received

    def handle_get(self):
        if self._filename.startswith("/index") or self._filename == "/":
            return self.code_ok + self.server_info + self.reply_no_service
        if self._filename.endswith("_call"):
            if self._uuid is None or self._token is None:
                return self.handle_invalid_format()
            token_find = self.find(self._uuid)
            if not (token_find is None ) and token_find == self._token:
                return self.handle_invalid_format()
            # call backend
            handler = default()
            backend_response = handler.handle_request(self._uuid, self._filename)
            if backend_response is None:
                return self.code_ok + self.server_info + self.backend_invalid
            else:
                return self.code_ok + self.server_info + backend_response
        return self.handle_invalid_format()

    def handle_invalid_format(self):
        return self.code_not_found + self.server_info + self.request_invalid

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, arg):
        print("Debug arg=", arg)
        self._request = arg
        if arg == "GET":
            self._reply = self.handle_get()
        else:
            if arg == "POST":
                self._reply = self.handle_post()
            else:
                self._reply = self.invalid_format()

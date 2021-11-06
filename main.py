import socket
import re
import sys
import os
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)

from data_process.default import default

from multiprocessing import Process

# 设置静态文件根目录
HTML_ROOT_DIR = "./html"
# 设置动态文件根目录
WSGI_PYTHON_DIR = "./data_process"

uuid_token_dic = {"0000": "2333"}
uuid_length = 4
token_length = 4

class HTTPServer(object):
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        self.server_socket.listen(128)
        while True:
            client_socket, client_address = self.server_socket.accept()
            # print("[%s, %s]用户连接上了" % client_address)
            handle_client_process = Process(target=self.handle_client, args=(client_socket,))
            handle_client_process.start()
            client_socket.close()

    def start_response(self, status, headers):
        response_headers = "HTTP/1.1 " + status + "\r\n"
        for header in headers:
            response_headers += "%s: %s\r\n" % header

        self.response_headers = response_headers

    def handle_client(self, client_socket):
        """
        处理客户端请求
        """
        # 获取客户端请求数据
        request_data = client_socket.recv(1024)
        print("request data:", request_data)
        request_lines = request_data.splitlines()
        for line in request_lines:
            print(line)

        # 解析请求报文
        request_start_line = request_lines[0]
        # 提取用户请求的文件名及请求方法
        file_name = re.match(r"\w+ +(/[^ ]*) ", request_start_line.decode("utf-8")).group(1)
        method = re.match(r"(\w+) +/[^ ]* ", request_start_line.decode("utf-8")).group(1)
        parameter_idx = file_name.find("?")
        parameter = file_name[parameter_idx + 1:]
        file_name = file_name[1:parameter_idx]
        print("file_name: ", file_name)
        print("parameter: ", parameter)
        print("method: ", method)
        response_start_line = "HTTP/1.1 200 OK\r\n"
        response_headers = "Server: My server\r\n"
        response_body = "Cannot understand"
        # 处理动态文件
        if method == "GET":
            if file_name.startswith("/index") or file_name == "/":
                response_body = "Have got your request but we do not provide user-readable service"
            else:
                if file_name.endswith("_call"):
                    # could be a valid method call
                    print("could be a valid call")
                    parameter_seperator_idx = parameter.find("&")
                    parameter_uuid_idx = parameter.find("uuid=")
                    parameter_token_idx = parameter.find("token=")
                    if (parameter_uuid_idx >= parameter_seperator_idx or parameter_token_idx < parameter_seperator_idx):
                        response_body = "Invalid request parameter format"
                    else:
                        parameter_uuid = parameter[parameter_uuid_idx + 5:parameter_seperator_idx]
                        parameter_token = parameter[parameter_token_idx + 6:]
                        print("uuid=", parameter_uuid)
                        print("token=", parameter_token)
                        if parameter_uuid in uuid_token_dic and uuid_token_dic[parameter_uuid] == parameter_token:
                            # a valid request, forward to data process
                            handler = default()
                            response_body = handler.handle_request(parameter_uuid, file_name)
                            if response_body == None:
                                response_body = "Invalid return value from backend"
                        else:
                            response_body = "Invalid uuid-token map"
                else:
                    response_start_line = "HTTP/1.1 404 Not Found\r\n"
                    response_body = "You are sending an invalid request"
        else:
            if method == "POST" and file_name == "append":
                # could be a dic update
                parameter_seperator_idx = parameter.find("&")
                parameter_uuid_idx = parameter.find("uuid=")
                parameter_token_idx = parameter.find("token=")
                if (parameter_uuid_idx >= parameter_seperator_idx or parameter_token_idx < parameter_seperator_idx):
                    response_body = "Invalid post parameter format"
                else:
                    parameter_uuid = parameter[parameter_uuid_idx + 5:parameter_seperator_idx]
                    parameter_token = parameter[parameter_token_idx + 6:]
                    print("uuid=", parameter_uuid)
                    print("token=", parameter_token)
                    uuid_token_dic[parameter_uuid] = parameter_token
                    response_body = "Map Received"
        response = response_start_line + response_headers + "\r\n" + response_body
        # print("response data:", response)

        # 向客户端返回响应数据
        client_socket.send(bytes(response, "utf-8"))

        # 关闭客户端连接
        client_socket.close()

    def bind(self, port):
        self.server_socket.bind(("", port))


def main():
    sys.path.insert(1, WSGI_PYTHON_DIR)
    http_server = HTTPServer()
    http_server.bind(8000)
    http_server.start()


if __name__ == "__main__":
    main()
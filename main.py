import socket
import re
import sys
import os

from controller import webController

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

        parameter_seperator_idx = parameter.find("&")
        parameter_uuid_idx = parameter.find("uuid=")
        parameter_token_idx = parameter.find("token=")
        if (parameter_uuid_idx >= parameter_seperator_idx or parameter_token_idx < parameter_seperator_idx):
            parameter_uuid = None
            parameter_token = None
        else:
            parameter_uuid = parameter[parameter_uuid_idx + 5:parameter_seperator_idx]
            parameter_token = parameter[parameter_token_idx + 6:]
        print("uuid=", parameter_uuid, ", token=", parameter_token)
        handler = webController()
        handler.web_params(file_name, parameter_token, parameter_uuid)
        handler.request = method


        response = handler.reply
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

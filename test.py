import sys
import os
import _thread
import time
import http.client

lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)

from main import main

def test():
    # this is a test
    time.sleep(1)
    print("wait finish, test begin")
    conn = http.client.HTTPConnection("localhost:8000")
    tot_pass = 0

    # functinal tests

    # invalid file
    conn.request("GET", "/doc")
    r1 = conn.getresponse()
    content = r1.read()
    print("status=", r1.status, "content=", content)
    conn.close()
    if r1.status == 404 and content == bytes("You are sending an invalid request", "ascii"):
        print("Test point 1 pass")
        tot_pass = tot_pass + 1
    else:
        print("Test point 1 fail")

    # valid file invalid parameter
    conn.request("GET", "/e_call?token=2333&uuid=0000")
    r1 = conn.getresponse()
    content = r1.read()
    print("status=", r1.status, "content=", content)
    conn.close()
    if r1.status == 200 and content == bytes("Invalid request parameter format", "ascii"):
        print("Test point 2 pass")
        tot_pass = tot_pass + 1
    else:
        print("Test point 2 fail")

    # valid file valid parameter
    conn.request("GET", "/j_call?uuid=0000&token=2333")
    r1 = conn.getresponse()
    content = r1.read()
    print("status=", r1.status, "content=", content)
    conn.close()
    if r1.status == 200 and content != bytes("Invalid request parameter format", "ascii"):
        print("Test point 3 pass")
        tot_pass = tot_pass + 1
    else:
        print("Test point 3 fail")
    # invalid file valid call
    conn.request("GET", "/e_call?uuid=0000&token=2333")
    r1 = conn.getresponse()
    content = r1.read()
    print("status=", r1.status, "content=", content)
    conn.close()
    if r1.status == 200 and content == bytes("Invalid return value from backend", "ascii"):
        print("Test point 4 pass")
        tot_pass = tot_pass + 1
    else:
        print("Test point 4 fail")

    # post and query
    conn.request("POST", "/append?uuid=0001&token=2334")
    r1 = conn.getresponse()
    content = r1.read()
    print("status=", r1.status, "content=", content)
    conn.close()
    if r1.status == 200 and content == bytes("Map Received", "ascii"):
        print("Test point 5 pass")
        tot_pass = tot_pass + 1
    else:
        print("Test point 5 fail")

    # valid file valid parameter
    conn.request("GET", "/j_call?uuid=0001&token=2334")
    r1 = conn.getresponse()
    content = r1.read()
    print("status=", r1.status, "content=", content)
    conn.close()
    if r1.status == 200 and content != bytes("Invalid request parameter format", "ascii"):
        print("Test point 6 pass")
        tot_pass = tot_pass + 1
    else:
        print("Test point 6 fail")

    print("Total poss", tot_pass, "points")

if __name__ == "__main__":
    print("starting test")

    try:
        _thread.start_new_thread(main, ())
        _thread.start_new_thread(test, ())
    except:
        print("Error: unable to start thread")
    while 1:
        pass
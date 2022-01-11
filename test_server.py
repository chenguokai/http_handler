import sys
import os
import _thread
import time
import http.client
import json

lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)

from main import main

def test_invalid_file():
    try:
        _thread.start_new_thread(main, ())
    except:
        assert "Error: unable to start thread"

    time.sleep(1)
    conn = http.client.HTTPConnection("localhost:8000")

    # invalid file
    conn.request("GET", "/doc")
    r1 = conn.getresponse()
    content = r1.read()
    print("status=", r1.status, "content=", content)
    conn.close()
    assert r1.status == 404 and content == bytes("You are sending an invalid request", "ascii")

def test_invalid_parameter():
    try:
        _thread.start_new_thread(main, ())
    except:
        assert "Error: unable to start thread"

    time.sleep(1)
    conn = http.client.HTTPConnection("localhost:8000")

    # valid file invalid parameter
    conn.request("GET", "/e_call?token=2333&uuid=0000")
    r1 = conn.getresponse()
    content = r1.read()
    print("status=", r1.status, "content=", content)
    conn.close()
    assert r1.status == 404 and content == bytes("You are sending an invalid request", "ascii")

def test_valid_request():
    try:
         _thread.start_new_thread(main, ())
    except:
        assert "Error: unable to start thread"

    time.sleep(1)
    conn = http.client.HTTPConnection("localhost:8000")

    # valid file invalid parameter
    conn.request("GET", "/j_call?uuid=0000&token=2333")
    r1 = conn.getresponse()
    content = r1.read()
    print("status=", r1.status, "content=", content)
    conn.close()
    assert r1.status == 200

'''

    # valid file valid parameter
    conn.request("GET", "/j_call?uuid=0000&token=2333")
    r1 = conn.getresponse()
    content = r1.read()
    print("status=", r1.status, "content=", content)
    conn.close()
    if r1.status == 404 and content == bytes("You are sending an invalid request", "ascii"):
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
    if r1.status == 404 and content == bytes("You are sending an invalid request", "ascii"):
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

    # post and query
    conn.request("POST", "/login?uuid=0001&token=2334")
    r1 = conn.getresponse()
    content = r1.read()
    print("status=", r1.status, "content=", content)
    conn.close()
    if r1.status == 200 and content == bytes("a valid data processing value\n", "ascii"):
        print("Test point 7 pass")
        tot_pass = tot_pass + 1
    else:
        print("Test point 7 fail")

    # post and query
    conn.request("GET", "/j_call?uuid=user1&token=2334")
    r1 = conn.getresponse()
    content = r1.read()
    print("status=", r1.status, "content=", content)
    conn.close()
    if r1.status == 200:
        print(json.loads(content))
        print("Test point 8 pass")
        tot_pass = tot_pass + 1
    else:
        print("Test point 8 fail")

    print("Total poss", tot_pass, "points")

if __name__ == "__main__":
    print("starting test")


    while 1:
        pass
        
'''
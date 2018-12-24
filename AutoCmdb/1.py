#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: 1.py
@time: 2018/12/14 15:44
@desc:
'''
import requests

def get_icp_2(IP):
    appcode = "1ba6f6e6fa3844d8b557887948d77c50"
    import ssl
    host = 'https://apis.map.qq.com/ws/location'
    path = '/v1/ip'
    method = 'GET'
    querys = 'ip={}&key={}'.format(IP,appcode)
    url = host + path + '?' + querys
    with requests.Session() as s:
        msg = s.get(url,headers={"Authorization": 'APPCODE ' + appcode},timeout=20000)
    print(msg.text)
    return msg.json()

if __name__ == '__main__':
    import time
    print(time.time())
    get_icp_2("114.247.50.2")
    print(time.time())
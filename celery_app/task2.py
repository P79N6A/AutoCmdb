#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: task2.py
@time: 2018/11/11 16:06
@desc:
'''
import time
from celery_app import app


@app.task
def multiply(x,y):
    time.sleep(4)
    return x * y
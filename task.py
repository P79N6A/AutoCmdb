#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: task.py
@time: 2018/11/10 17:18
@desc:
'''
import time

from celery import Celery


broker = 'redis://127.0.0.1:6379/1'
backend = 'redis://127.0.0.1:6379/2'

app = Celery("my_task",broker=broker,backend=backend)


@app.task
def add(x,y):
    print("enter task")
    time.sleep(4)
    return x + y


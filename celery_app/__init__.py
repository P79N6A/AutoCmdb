#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: __init__.py.py
@time: 2018/11/11 16:05
@desc:
'''
from celery import Celery


app = Celery("demo")


app.config_from_object("config.celeryconfig") #通过celery实例加载


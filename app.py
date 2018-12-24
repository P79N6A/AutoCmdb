#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: app.py
@time: 2018/11/10 17:06
@desc:
'''




from celery_app import task1,task2



print("start..")
task1.add.delay(2,3)
task2.multiply.delay(4,5)
print("end....")
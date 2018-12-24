#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: nom.py
@time: 2018/12/17 14:24
@desc:
'''
# get_update_db("nom.12","nom")
from log_analyse.services.getIP import get_update_db
from multiprocessing.dummy import Pool as ThreadPool
pool = ThreadPool(4)
try:
    d = pool.apply_async(get_update_db,args=("nom.12","nom"),kwds={"host":"47.244.101.148",
                                                                   "port":26381,
                                                                   "db":3,
                                                                   "password":"167eb9bac705aa3c295f"})
except Exception as e:
    print(e)
pool.close()
pool.join()
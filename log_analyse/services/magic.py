#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: magic.py
@time: 2018/12/19 13:49
@desc:
'''
from log_analyse.services.getIP import get_update_db,get_up_db
from multiprocessing.dummy import Pool as ThreadPool
if __name__ == '__main__':
    pool = ThreadPool(4)
    # get_update_db("magic.12","magic",host="47.244.101.148",port=26381,db=4,password="167eb9bac705aa3c295f")
    d = pool.apply_async(get_update_db, args=("magic.12","magic"), kwds={"host": "47.244.101.148",
                                                                      "port": 26381,
                                                                      "db": 4,
                                                                      "password": "167eb9bac705aa3c295f"})
    pool.close()
    pool.join()
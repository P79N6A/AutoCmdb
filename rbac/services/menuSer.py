#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: menuSer.py
@time: 2018/12/11 11:35
@desc:
'''
import os,django,copy
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoCmdb.settings")
django.setup()
from rbac.models import Menu


def menu_select(menu_objs):
    """
    菜单管理 下拉返回格式化json数据
    :return:
    """
    select_list = []
    select_dicc = {
        "id":0,
        "name":"",
        "open":True,
        "children":[

        ],
        "checked": True}
    select_dics = {
        "id":0,
        "name":"",
        "open":True,
        "children":[

        ],
        "checked": True
    }

    print(menu_objs)
    for i in menu_objs:
        if i["parent_id"] == None:
            select_dics["id"] = i["id"]
            select_dics["name"] = i["caption"]
            select_dics["open"] = True
            select_dics["checked"] = True
            select_list.append(select_dics)
            for j in menu_objs:
                select_dict = copy.deepcopy(select_dicc)
                if j["parent_id"] == i["id"]:
                    select_dict["id"] = j["id"]
                    select_dict["name"] = j["caption"]
                    select_dict["open"] = False
                    select_dict["checked"] = True
                    select_dics["children"].append(select_dict)
                    for z in menu_objs:
                        select_dic2 = copy.deepcopy(select_dicc)
                        if z["parent_id"] == j["id"]:
                            select_dic2["id"] = z["id"]
                            select_dic2["name"] = z["caption"]
                            select_dic2["open"] = False
                            select_dic2["checked"] = True
                            select_dict["children"].append(select_dic2)
                            for m in menu_objs:
                                select_dic3 = copy.deepcopy(select_dicc)
                                if m["parent_id"] == z["id"]:
                                    select_dic3["id"] = m["id"]
                                    select_dic3["name"] = m["caption"]
                                    select_dic3["open"] = False
                                    select_dic3["checked"] = True
                                    select_dic3.pop("children")
                                    select_dic2["children"].append(select_dic3)
    print(select_list)
    return select_list


# if __name__ == '__main__':
#     menu_select()
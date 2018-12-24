#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: othHandler.py
@time: 2018/11/21 11:50
@desc:
'''
import datetime
import json
from rbac.models import User,Role,User2Role,Menu,Permission,Action,Permission2Action2Role
from django.db.models import F, Q
from django.shortcuts import render,HttpResponse,redirect

def utc2local( UTC_FORMAT,utc_dtm ):
    # UTC 时间转本地时间（ +8:00 ）
    # UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    utcTime = datetime.datetime.strptime(utc_dtm, UTC_FORMAT)
    localtime = utcTime + datetime.timedelta(hours=8)
    print(localtime)
    return localtime


def ali_wrap(func):
    """
    阿里云基本返回装饰器
    :param func:
    :return:
    """
    def wrapper(self, *args, **kwargs):
        request = func(self, *args, **kwargs)
        if isinstance(request,tuple):
            req = request[0]
            param = request[1]
            for k,v in param.items():
                if v:
                    exec(k + "={}".format(v))
                    print(v)
                    if hasattr(req, "set_{}".format(k)):
                        getattr(req, "set_{}".format(k), )(v)
        else:
            req = request
        req.set_accept_format("json")
        result = json.loads(self.clt.do_action(req))
        return result
    return wrapper


def ali_rbac(**vkargs):
    def validate(func):
        def wrapper(self,request, *args, **kwargs):
            result = func(self, request, *args, **kwargs)
            rbac_menu_permission = request.session.get("rbac_permission_session_key")
            username = request.session.get("user_info").get("username")
            role_caption = User2Role.objects.values("role__caption").filter(user__username=username).first()
            rbac_list = list(Permission2Action2Role.objects.values("permission__menu", "action__code", "permission__url",
                                                                   "permission__caption", "permission__menu__caption",
                                                                   "permission__menu__parent").filter(
                Q(permission__url__in=rbac_menu_permission.keys()) & Q(role__caption=role_caption["role__caption"])))
            for i in rbac_list:
                i["permission__url"] = i["permission__url"].split("$")[0]

            url = vkargs["url"]
            return render(request, url, locals())
        return wrapper
    return validate


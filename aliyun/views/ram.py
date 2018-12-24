#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: ram.py
@time: 2018/11/26 9:58
@desc:
'''
import json
from django.views import View
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from aliyun.models import AliAccount,Region
from aliyun.forms import ali_account_form
from aliyun.service import aliHandle,othHandler,aliRam
from django.core.cache import cache
from aliyun.views import account
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rbac.models import User, Role, User2Role, Menu, Permission, Action, Permission2Action2Role
from django.db.models import F, Q

class RAMView(View):
    dic_news = {
        "state": 0,
        "code": 0
        , "msg": ""
        , "count": 3000000
        , "data": []}

    def post(self,request, *args, **kwargs):
        print(request.POST)
        suppUserId = request.POST.get("suppUserId")
        limit = request.POST.get("pageSize")  # 当页有几列
        page = request.POST.get("pageStart")  # 当前是多少页
        act = account.get_act(suppUserId)
        if act["state"]:
            ram = aliRam.aliRam(act["accessKey"],act["accessSecret"])
            print(ram.list_users())
            ram_user_list = ram.list_users()["Users"]["User"]
            print(ram_user_list)
            for i in ram_user_list:
                i["accountName"] = suppUserId
            self.dic_news["data"] = ram_user_list
            self.dic_news["count"] = len(ram_user_list)
            paginator = Paginator(self.dic_news["data"], limit)
            self.dic_news["data"] = paginator.page(page).object_list
            return JsonResponse(self.dic_news)

    def get(self, request, *args, **kwargs):
        rbac_menu_permission = request.session.get("rbac_permission_session_key")
        username = request.session.get("user_info").get("username")
        role_caption = User2Role.objects.values("role__caption").filter(user__username=username).first()
        rbac_list = list(Permission2Action2Role.objects.values("permission__menu", "action__code", "permission__url",
                                                               "permission__caption", "permission__menu__caption",
                                                               "permission__menu__parent").filter(
            Q(permission__url__in=rbac_menu_permission.keys()) & Q(role__caption=role_caption["role__caption"])))
        for i in rbac_list:
            i["permission__url"] = i["permission__url"].split("$")[0]
        accountName = request.GET.get("accountName")
        return render(request, "aliyun/ram/index.html", locals())


class getRamInfo(View):

    def get(self, request, *args, **kwargs):
        rbac_menu_permission = request.session.get("rbac_permission_session_key")
        username = request.session.get("user_info").get("username")
        role_caption = User2Role.objects.values("role__caption").filter(user__username=username).first()
        rbac_list = list(Permission2Action2Role.objects.values("permission__menu", "action__code", "permission__url",
                                                               "permission__caption", "permission__menu__caption",
                                                               "permission__menu__parent").filter(
            Q(permission__url__in=rbac_menu_permission.keys()) & Q(role__caption=role_caption["role__caption"])))
        for i in rbac_list:
            i["permission__url"] = i["permission__url"].split("$")[0]
        accountName = request.GET.get("accountName")
        UserName = request.GET.get("UserName")
        act = account.get_act(accountName)
        if act["state"]:
            ram = aliRam.aliRam(act["accessKey"],act["accessSecret"])
            ram_info = ram.get_user(UserName)
            ram_acc = ram.list_accesskeys(UserName)
        return render(request,"aliyun/ram/info.html",locals())


class setAccessStatus(View):
    def post(self, request, *args, **kwargs):
        accessKeyID = request.POST.get("accessKeyID")
        Status = request.POST.get("Status")
        UserName = request.POST.get("UserName")
        accountName = request.POST.get("accountName")

        if Status == "启用":
            Status = "Active"
        elif Status == "禁用":
            Status = "Inactive"
        act = account.get_act(accountName)
        if act["state"]:
            ram = aliRam.aliRam(act["accessKey"], act["accessSecret"])
            accesskey_set_status = ram.update_accesskey(accessKeyID,Status,UserName)
            print(accesskey_set_status)
            return JsonResponse({"state":1})


class delAccessKey(View):
    def post(self, request, *args, **kwargs):
        accessKeyID = request.POST.get("accessKeyID")
        UserName = request.POST.get("UserName")
        accountName = request.POST.get("accountName")
        act = account.get_act(accountName)
        if act["state"]:
            ram = aliRam.aliRam(act["accessKey"], act["accessSecret"])
            accesskey = ram.delete_accesskey(accessKeyID,UserName)
            print(accesskey)
            return JsonResponse({"state":1})


class addAccessKey(View):
    def post(self, request, *args, **kwargs):
        UserName = request.POST.get("UserName")
        accountName = request.POST.get("accountName")
        act = account.get_act(accountName)
        if act["state"]:
            ram = aliRam.aliRam(act["accessKey"], act["accessSecret"])
            accessKey = ram.create_accesskey(UserName)
            if accessKey.get("AccessKey"):
                return JsonResponse({"state":1})
            else:
                return JsonResponse({"state": 0})

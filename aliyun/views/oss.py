#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: oss.py
@time: 2018/11/30 10:41
@desc:
'''
import json
from django.views import View
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from aliyun.models import AliAccount,Region
from aliyun.service import aliHandle
from django.core.cache import cache
from aliyun.views import account
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class OssView(View):
    dic_news = {
        "state": 0,
        "code": 0
        , "message": ""
        , "count": 3000000
        , "data": []}

    def post(self,request, *args, **kwargs):
        print(request.POST)
        suppUserId = request.POST.get("suppUserId")
        limit = request.POST.get("pageSize")  # 当页有几列
        page = request.POST.get("pageStart")  # 当前是多少页
        act = account.get_act(suppUserId)
        if act["state"]:
            oss = aliHandle.AliOss(act["accessKey"],act["accessSecret"])
            oss_list = oss.get_oss_list()
            print(type(oss_list),oss_list)
            if isinstance(oss_list,dict):
                print(1)
                self.dic_news["message"] = oss_list.get("details").get("Message")
                self.dic_news["state"] = oss_list.get("status")
                return JsonResponse(self.dic_news)
            for i in oss_list:
                i["accountName"] = suppUserId
            self.dic_news["state"] = 200
            self.dic_news["data"] = oss_list
            self.dic_news["count"] = len(oss_list)
            # paginator = Paginator(self.dic_news["data"], limit)
            # self.dic_news["data"] = paginator.page(page).object_list
            return JsonResponse(self.dic_news)

    def get(self, request, *args, **kwargs):
        accountName = request.GET.get("accountName")
        print(accountName)
        return render(request, "aliyun/oss/index.html", locals())


class getOssInfo(View):

    def get(self, request, *args, **kwargs):
        accountName = request.GET.get("accountName")
        bucketName = request.GET.get("bucketName")
        act = account.get_act(accountName)
        if act["state"]:
            oss = aliHandle.AliOss(act["accessKey"],act["accessSecret"])
            oss_info = oss.get_bucket_info(bucket_name=bucketName)
            print(oss_info.get("acl").__dict__)
        return render(request,"aliyun/oss/info.html",locals())





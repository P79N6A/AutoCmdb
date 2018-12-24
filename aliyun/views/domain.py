#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: domain.py
@time: 2018/11/13 11:28
@desc:
'''
import json
import requests
import re
from multiprocessing import Pool
from aliyun.service import aliHandle
from django.views import View
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from aliyun.models import AliAccount,Region
from django.core.cache import cache
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from aliyun.forms import ali_account_form
from aliyun.service import getIcp
from rbac.cbv.views import RbacView
from aliyun.service.othHandler import ali_rbac


def get_icp(domainName):
    dic = {}
    url = 'https://www.sojson.com/api/beian/{}'.format(domainName)
    msg = requests.get(url)
    print(msg)
    return msg


def get_ali_domain(accountName,limit,page,orderId):
    import time
    allAct = AliAccount.objects.values("accessKey", "accessSecret").filter(accountName=accountName).first()
    domain = aliHandle.AliyunDomain(allAct["accessKey"], allAct["accessSecret"])
    dic_domain = domain.get_second_domain(limit, page)
    list_domain = dic_domain["Data"]["Domain"]
    print(list_domain)
    from django.urls import reverse
    import re
    new_list = []
    for i in list_domain:
        if orderId:
            new_i = i
            for k, v in i.items():
                try:
                    if k == "DomainName":
                        ret = re.findall("{}".format(orderId), "{}".format(v))
                        print(ret)
                        if ret:
                            new_list.append(new_i)
                        else:
                            if new_i in new_list:
                                new_list.remove(new_i)
                                new_i = {}
                            else:
                                new_i = {}
                    else:
                        pass
                except Exception as e:
                    print(e)
        else:
            new_i = i
            new_list = list_domain
        new_i["accountName"] = accountName
        v = reverse("get_domain_info")
        new_i["domainName"] = new_i.get("DomainName")
        new_i["ZhRegistrantOrganization"] = domain.get_domain_info(new_i.get("InstanceId"))["ZhRegistrantOrganization"]
       #  new_i["ZhRegistrantOrganization"] = p1.apply_async(func=domain.get_domain_info,args=(new_i.get("InstanceId"),)).get()["ZhRegistrantOrganization"]
        # beian_info = getIcp.get_icp_2(new_i.get("domainName"))
        # beian_obj = beian_info.get("showapi_res_body").get("obj")
        #
        # new_i["beian_nowIcp"] = beian_obj["num"]
        # new_i["beian_sitename"] = beian_obj["sys_name"]
        # new_i["beian_nature"] = beian_obj["type"]
        new_i["DomainName"] = "<a id='{}' href='{}?accountName={}&InstanceId={}'>{}</a>".format(
            new_i.get("DomainName"),
            v, accountName, new_i.get("InstanceId"),
            new_i.get("DomainName"))
        if new_i.get("DomainAuditStatus") == "SUCCEED":
            new_i["DomainAuditStatus"] = "实名认证成功"
        elif new_i.get("DomainAuditStatus") == "FAILED":
            new_i["DomainAuditStatus"] = "实名认证失败"
        elif new_i.get("DomainAuditStatus") == "AUDITING":
            new_i["DomainAuditStatus"] = "审核中"
        else:
            new_i["DomainAuditStatus"] = "未实名认证"
        if new_i.get("DomainStatus") == "1":
            new_i["DomainStatus"] = "急需续费"
        elif new_i.get("DomainStatus") == "2":
            new_i["DomainStatus"] = "急需赎回"
        else:
            new_i["DomainStatus"] = "正常"
        if new_i.get("ExpirationDateStatus") == "1":
            new_i["ExpirationDateStatus"] = "域名未过期"
        else:
            new_i["ExpirationDateStatus"] = "域名已过期"
        if new_i.get("RegistrantType") == "1":
            new_i["RegistrantType"] = "个人"
        else:
            new_i["RegistrantType"] = "企业"
        # dic_new.get("data").append(new_i)
    return new_list,dic_domain


class aliSecondDomains(RbacView,View):

    def post(self, request, *args, **kwargs):
            dic_news = {
                "state": 0,
                "code": 0
                , "msg": ""
                , "count": 3000000
                , "data": []}
            orderId = request.POST.get("orderId")
            print(2222,orderId)
            accountName = request.POST.get("accountName")
            limit = request.POST.get("pageSize")  # 当页有几列
            page = request.POST.get("pageStart")  # 当前是多少页
            count = 0
            if accountName == "全部":
                z = cache.get("all_domain")
                if not z:
                    act_list = list(AliAccount.objects.values("accountName").exclude(accountName="全部").all())
                    print(act_list)
                    for k in act_list:
                        dic_new_obj,dic_domain = get_ali_domain(accountName=k["accountName"] ,limit=limit,page=page,orderId=orderId)
                        # dic_new_obj,dic_domain = gevent.spawn(get_ali_domain,{"accountName":k["accountName"] ,"limit":1000,"page":page,"orderId":orderId,})
                        for z in dic_new_obj:
                            dic_news["data"].append(z)
                        count += dic_domain["TotalItemNum"]
                    if dic_news.get("data"):
                        # dic_news["data"] = paginator.page(page).object_list
                        dic_news["count"] = count
                        dic_news["state"] = 0
                    else:
                        dic_news["count"] = count
                        dic_news["state"] = 1
                    cache.set("all_domain",dic_news,timeout=None)
                    paginator = Paginator(dic_news["data"], limit)
                    dic_news["data"] = paginator.page(page).object_list
                    return JsonResponse(dic_news)
                else:
                    list_domain = []
                    if orderId:
                        for o in z["data"]:
                            # print(orderId,o["domainName"])
                            d = re.findall(orderId, o["domainName"])

                            if d:
                                list_domain.append(o)
                            else:
                                pass
                        z["data"] = list_domain
                    paginator = Paginator(z["data"], limit)
                    z["data"] = paginator.page(page).object_list
                    return JsonResponse(z)
            else:
                z = cache.get("domainName_{}".format(accountName))
                if not z:
                    dic_new_obj,dic_domain = get_ali_domain(accountName=accountName, limit=limit, page=page, orderId=orderId)
                    print(dic_new_obj)
                    for z in dic_new_obj:
                        dic_news["data"].append(z)
                    count += dic_domain["TotalItemNum"]
                    if dic_news.get("data"):
                        # dic_news["data"] = paginator.page(page).object_list
                        dic_news["count"] = count
                        dic_news["state"] = 0
                    else:
                        dic_news["count"] = count
                        dic_news["state"] = 1
                    cache.set("domainName_{}".format(accountName), dic_news,timeout=None)
                    paginator = Paginator(dic_news["data"], limit)
                    dic_news["data"] = paginator.page(page).object_list
                    return JsonResponse(dic_news)
                else:
                    list_domain = []
                    if orderId:
                        for o in z["data"]:
                            # print(orderId,o["domainName"])
                            d = re.findall(orderId, o["domainName"])
                            if d:
                                list_domain.append(o)
                            else:
                                pass
                        z["data"] = list_domain
                    paginator = Paginator(z["data"], limit)
                    z["data"] = paginator.page(page).object_list
                    return JsonResponse(z)


class domainViews(RbacView,View):
    """
    查看阿里ECS资源
    """
    @ali_rbac(url='aliyun/domain/index.html')
    def get(self, request, *args, **kwargs):
        allAct = AliAccount.objects.values("accountName")
        return render(request, 'aliyun/domain/index.html', locals())


class domainInfo(RbacView,View):

    def get(self, request, *args, **kwargs):
        print(request.GET)
        accountName = request.GET.get("accountName")
        InstanceId = request.GET.get("InstanceId")

        allAct = AliAccount.objects.values("accessKey","accessSecret").filter(accountName=accountName).first()

        domain = aliHandle.AliyunDomain(allAct["accessKey"],allAct["accessSecret"])
        result = domain.get_domain_info(InstanceId)
        domainName = result["DomainName"]
        new_dic = {}

        return render(request, 'aliyun/domain/domain_info.html', locals())


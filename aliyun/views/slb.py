#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: slb.py
@time: 2018/11/21 17:33
@desc:
'''

import json
from django.views import View
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from aliyun.models import AliAccount,Region
from aliyun.forms import ali_account_form
from aliyun.service import aliHandle,othHandler
from django.core.cache import cache
from aliyun.views import account
from aliyun.service.othHandler import ali_rbac
from rbac.models import User, Role, User2Role, Menu, Permission, Action, Permission2Action2Role
from django.db.models import F, Q
from rbac.cbv.views import RbacView


class SlbView(RbacView,View):
    @ali_rbac(url="aliyun/slb/index.html")
    def get(self, request, *args, **kwargs):

        return render(request,"aliyun/slb/index.html",locals())


def get_ali_domain(accountName,limit,page,orderId):
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
                        # print(ret)
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


class getSlbView(RbacView,View):

    def post(self, request, *args, **kwargs):
        dic_news = {
            "state": 0,
            "code": 0
            , "msg": ""
            , "count": 3000000
            , "data": []}
        accountName = request.POST.get("suppUserId")
        regionId = request.POST.get("suppId")
        pageStart = request.POST.get("pageStart")
        pageSize = request.POST.get("pageSize")
        allAct = AliAccount.objects.values("accessKey", "accessSecret").filter(accountName=accountName).first()
        domain = aliHandle.AliyunSlb(allAct["accessKey"], allAct["accessSecret"],regionId)
        result = domain.get_slbs(pageStart=pageStart,pageSize=pageSize)["LoadBalancers"]["LoadBalancer"]
        dic_news["count"] = len(result)
        dic_news["data"] = result
        for va in dic_news["data"]:
            va["accountName"] = accountName
            if va["NetworkType"] == "vpc":
                va["NetworkType"] = "专有网络实例"
            elif va["NetworkType"] == "classic":
                va["NetworkType"] = "经典网络实例"
            else:
                pass
            if va["LoadBalancerStatus"] == "inactive":
                va["LoadBalancerStatus"] = "已停止"
            elif va["LoadBalancerStatus"] == "active":
                va["LoadBalancerStatus"] = "运行中"
            elif va["LoadBalancerStatus"] == "locked":
                va["LoadBalancerStatus"] = "锁定"
            else:
                pass
            if va["InternetChargeType"] == "4":
                va["InternetChargeType"] = "按使用流量"
            elif va["InternetChargeType"] == "3":
                va["InternetChargeType"] = "按使用带宽"
            else:
                pass

        return JsonResponse(dic_news)


class getSlbInfo(RbacView,View):

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
        RegionId = request.GET.get("RegionId")
        LoadBalancerId = request.GET.get("LoadBalancerId")
        act = account.get_act(accountName)
        if act["state"]:
            slb = aliHandle.AliyunSlb(act["accessKey"],act["accessSecret"],RegionId)
            slb_info = slb.get_slb(LoadBalancerId)
        return render(request,"aliyun/slb/info.html",locals())

    def post(self,request, *args, **kwargs):
        dic_news = {
            "state": 0,
            "code": 0
            , "msg": ""
            , "count": 3000000
            , "data": []}
        accountName = request.POST.get("accountName") # 账号名
        RegionId = request.POST.get("RegionId") # 可用区
        LoadBalancerId = request.POST.get("LoadBalancerId") # lbID
        act = account.get_act(accountName)
        if act["state"]:
            domain = aliHandle.AliyunSlb(act["accessKey"], act["accessSecret"], RegionId)
            result = domain.get_slb(LoadBalancerId)

            # dic_news["count"] = len(result)
            # dic_news["data"] = result
            listener = result["ListenerPortsAndProtocol"]["ListenerPortAndProtocol"]
            dic_news["data"] = listener
            for i in dic_news["data"]:
                print(i.get("ForwardPort"))
                z = domain.get_slb_listener(action=i.get("ListenerProtocol"),LoadBalancerId=LoadBalancerId,ListenerPort=i.get("ListenerPort"))
                if z.get("Scheduler") == "wrr":
                    z["Scheduler"] = "加权轮询"
                elif z.get("Scheduler") == "rr":
                    z["Scheduler"] = "轮询"
                elif z.get("Scheduler") == "wlc":
                    z["Scheduler"] = "加权最少连接"
                else:
                    pass
                i.update(z)

            return JsonResponse(dic_news)


class getSlbServerGroup(RbacView,View):
    def post(self,request, *args, **kwargs):
        dic_news = {
            "state": 0,
            "code": 0
            , "msg": ""
            , "count": 3000000
            , "data": []}
        accountName = request.POST.get("accountName")  # 账号名
        RegionId = request.POST.get("RegionId")  # 可用区
        LoadBalancerId = request.POST.get("LoadBalancerId")  # lbID
        act = account.get_act(accountName)
        if act["state"]:
            domain = aliHandle.AliyunSlb(act["accessKey"], act["accessSecret"], RegionId)
            result = domain.get_vservergroups(LoadBalancerId)

            dic_news["data"] = result.get("VServerGroups").get("VServerGroup")
            return JsonResponse(dic_news)


class getSlbServerGroupS(RbacView,View):

    def post(self, request, *args, **kwargs):
        dic_news = {
            "state": 0,
            "code": 0
            , "msg": ""
            , "count": 3000000
            , "data": []}
        accountName = request.POST.get("accountName")  # 账号名
        RegionId = request.POST.get("RegionId")  # 可用区
        VServerGroupId = request.POST.get("VServerGroupId")  # lbID
        act = account.get_act(accountName)
        if act["state"]:
            domain = aliHandle.AliyunSlb(act["accessKey"], act["accessSecret"], RegionId)
            jj = domain.get_vserver_group_attr(VServerGroupId)
            print(jj)
            return JsonResponse(dic_news)

    def get(self, request, *args, **kwargs):
        accountName = request.GET.get("accountName")  # 账号名
        RegionId = request.GET.get("RegionId")  # 可用区
        VServerGroupId = request.GET.get("VServerGroupId")  # 可用区
        return render(request,"aliyun/slb/v-server-group.html",locals())


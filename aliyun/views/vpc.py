#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: vpc.py
@time: 2018/11/27 15:23
@desc:
'''
import json
from django.views import View
from django.shortcuts import render,HttpResponse,reverse
from django.http import JsonResponse
from aliyun.views import account
from aliyun.service import aliHandle,othHandler,aliVpc
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rbac.models import User, Role, User2Role, Menu, Permission, Action, Permission2Action2Role
from django.db.models import F, Q
from rbac.cbv.views import RbacView


class VPCView(RbacView,View):
    dic_news = {
        "state": 0,
        "code": 0
        , "msg": ""
        , "count": 3000000
        , "data": []}

    def post(self, request, *args, **kwargs):
        print(request.POST)
        suppUserId = request.POST.get("suppUserId")
        regionId = request.POST.get("suppId")
        limit = request.POST.get("pageSize")  # 当页有几列
        page = request.POST.get("pageStart")  # 当前是多少页
        act = account.get_act(suppUserId)
        if act["state"]:
            vpc = aliVpc.aliVpc(act["accessKey"], act["accessSecret"],regionId)
            vpc_list = vpc.vpc_list(PageNumber=page,PageSize=limit)
            print(1)
            for i in vpc_list["Vpcs"]["Vpc"]:
                vroute_url = reverse("ali_vpc_route")+\
                             "?accountName={}&RegionId={}&VpcId={}".format(
                                 suppUserId,
                                 regionId,
                                 i.get("VpcId"))
                print(vroute_url)
                vswitch_url = reverse("ali_vpc_switch")+\
                              "?accountName={}&RegionId={}&VpcId={}".format(
                                  suppUserId,
                                  regionId,
                                  i.get("VpcId"))
                vroute = "<a href='{}'>{}</a>".format(vroute_url,len(i.get("RouterTableIds").get("RouterTableIds")))
                vswitch = "<a href='{}'>{}</a>".format(vswitch_url, len(i.get("VSwitchIds").get("VSwitchId")))
                i["vRoute_count"] = vroute
                i["vSwitch_count"] = vswitch
                i["accountName"] = suppUserId
            self.dic_news["data"] = vpc_list["Vpcs"]["Vpc"]
            self.dic_news["count"] = len(vpc_list)
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
        RegionId = request.GET.get("RegionId")
        return render(request, "aliyun/vpc/index.html", locals())


class VpcRouteView(RbacView,View):
    dic_news = {
        "state": 0,
        "code": 0
        , "msg": ""
        , "count": 3000000
        , "data": []}

    def post(self, request, *args, **kwargs):
        print(request.POST)
        suppUserId = request.POST.get("suppUserId")
        regionId = request.POST.get("suppId")
        limit = request.POST.get("pageSize")  # 当页有几列
        page = request.POST.get("pageStart")  # 当前是多少页
        VpcId = request.POST.get("VpcId")
        # if VpcId == "0":
        #     VpcId = 0
        act = account.get_act(suppUserId)
        if act["state"]:
            print(regionId)
            vpc_route = aliVpc.aliVpc(act["accessKey"], act["accessSecret"],regionId)

            vpc_route_list = vpc_route.get_route_list(PageNumber=page,PageSize=limit,VpcId=VpcId)
            for i in vpc_route_list["RouterTableList"]["RouterTableListType"]:
                i["accountName"] = suppUserId
                i["RegionId"] = regionId
            self.dic_news["data"] = vpc_route_list["RouterTableList"]["RouterTableListType"]
            self.dic_news["count"] = len(vpc_route_list)
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
        RegionId = request.GET.get("RegionId")
        VpcId = request.GET.get("VpcId")
        if not VpcId:
            VpcId = 0
        print(accountName,RegionId,VpcId)
        return render(request, "aliyun/vpc/route.html", locals())


class VpcSwitchView(RbacView,View):
    dic_news = {
        "state": 0,
        "code": 0
        , "msg": ""
        , "count": 3000000
        , "data": []}

    def post(self, request, *args, **kwargs):
        print(request.POST)
        suppUserId = request.POST.get("suppUserId")
        regionId = request.POST.get("suppId")
        limit = request.POST.get("pageSize")  # 当页有几列
        page = request.POST.get("pageStart")  # 当前是多少页
        VpcId = request.POST.get("VpcId")
        act = account.get_act(suppUserId)
        if act["state"]:
            vpc_route = aliVpc.aliVpc(act["accessKey"], act["accessSecret"],regionId)
            vpc_route_list = vpc_route.get_switch_list(PageNumber=page,PageSize=limit,VpcId=VpcId)
            for i in vpc_route_list["VSwitches"]["VSwitch"]:
                i["accountName"] = suppUserId
                i["RegionId"] = regionId
                i["RouteTableId"] = i.get("RouteTable").get("RouteTableId")
                i["RouteTableType"] = i.get("RouteTable").get("RouteTableType")
            self.dic_news["data"] = vpc_route_list["VSwitches"]["VSwitch"]
            self.dic_news["count"] = len(vpc_route_list)
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
        RegionId = request.GET.get("RegionId")
        VpcId = request.GET.get("VpcId")
        if not VpcId:
            VpcId = 0
        return render(request, "aliyun/vpc/switch.html", locals())


class VpcEipView(RbacView,View):
    dic_news = {
        "state": 0,
        "code": 0
        , "msg": ""
        , "count": 3000000
        , "data": []}

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
        return render(request, "aliyun/vpc/eips.html", locals())

    def post(self, request, *args, **kwargs):
        print(request.POST)
        suppUserId = request.POST.get("suppUserId")
        regionId = request.POST.get("suppId")
        limit = request.POST.get("pageSize")  # 当页有几列
        page = request.POST.get("pageStart")  # 当前是多少页
        print(limit,page,1111)
        act = account.get_act(suppUserId)
        status = {"Associating":"绑定中",
                  "Unassociating":"解绑中",
                  "InUse":"已分配",
                  "Available":"可用"}

        if act["state"]:
            vpc_eip = aliVpc.aliVpc(act["accessKey"], act["accessSecret"],regionId)
            vpc_eip_list = vpc_eip.get_eip_addresses(PageNumber=page,PageSize=limit)
            print(vpc_eip_list)
            utcBandwidth = "%Y-%m-%dT%H:%M:%SZ"
            utcTraffic = "%Y-%m-%dT%H:%MZ"
            for i in vpc_eip_list["EipAddresses"]["EipAddress"]:
                InternetChargeType = {
                    "PayByTraffic":"共享带宽",
                    "PayByBandwidth":"按固定带宽计费"
                }
                times = {"PayByTraffic":"后付费{}创建",
                         "PayByBandwidth": "预付费{}到期"}
                i["accountName"] = suppUserId
                i["Status"] = status.get(i.get("Status"))
                i["RegionId"] = regionId
                i["BandwidthAndType"] = "{} Mbps\n{}".format(i.get("Bandwidth"),InternetChargeType.get(i.get("InternetChargeType")))
                if i.get("ExpiredTime"):
                    i["times"] = times.get(i.get("InternetChargeType")).format(othHandler.utc2local(utcTraffic,i.get("ExpiredTime")))
                else:
                    i["times"] = times.get(i.get("InternetChargeType")).format(
                        othHandler.utc2local(utcBandwidth, i.get("AllocationTime")))
            self.dic_news["data"] = vpc_eip_list["EipAddresses"]["EipAddress"]
            self.dic_news["count"] = vpc_eip_list["TotalCount"]
            print(limit,page)

            paginator = Paginator(self.dic_news["data"], limit)
            try:
                self.dic_news["data"] = paginator.page(page).object_list
                print(self.dic_news["data"])
            except Exception as e:
                self.dic_news["data"] = paginator.page(paginator.num_pages).object_list

            return JsonResponse(self.dic_news)

#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: rds.py
@time: 2018/11/19 16:23
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
from django.contrib.auth.decorators import login_required
from aliyun.service.othHandler import ali_rbac
from rbac.models import User, Role, User2Role, Menu, Permission, Action, Permission2Action2Role
from django.db.models import F, Q
from rbac.cbv.views import RbacView



class clearDomainCache(RbacView,View):

    def post(self, request, *args, ** kwargs):
        accountName = request.POST.get("accountName")
        if accountName:
            if accountName == "全部":
                cache.delete_pattern("all_domain")
            else:
                cache.delete_pattern("domainName_{}".format(accountName))
            code = 0
        else:
            code = 1
        return JsonResponse({"code":code})


class RdsView(RbacView,View):

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
        return render(request,"aliyun/rds/index.html",locals())


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


class getRdsView(RbacView,View):

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
        domain = aliHandle.AliyunRDS(allAct["accessKey"], allAct["accessSecret"],regionId)
        result = domain.get_rds(pageStart=pageStart,pageSize=pageSize)["Items"]["DBInstance"]
        for i in result:
            i["accountName"] = accountName
            i["EngineT"] = i["Engine"] + i["EngineVersion"]
            i["create_time"] = i["CreateTime"]
            if i["PayType"] == "Prepaid":
                i["pay_type"] = "预付费（包年包月"
            else:
                i["pay_type"] = "按量付费"
        dic_news["count"] = len(result)
        dic_news["data"] = result
        print(dic_news)
        return JsonResponse(dic_news)



class getRdsInfo(RbacView,View):

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
        DBInstanceId = request.GET.get("DBInstanceId")
        act = account.get_act(accountName)
        if act["state"]:
            rds = aliHandle.AliyunRDS(act["accessKey"],act["accessSecret"],RegionId)
            rds_info = rds.get_rds_instace(DBInstanceId)["Items"]["DBInstanceAttribute"][0]
            rds_array_list =rds.get_rds_IP_ArrayList(DBInstanceId)["Items"]["DBInstanceIPArray"]
            rds_info["DBInstanceIPArray"] = rds_array_list
            if rds_info["Category"] == "Basic":
                rds_info["Category"] = "基础版"
            elif rds_info["Category"] == "HighAvailability":
                rds_info["Category"] = "高可用版"
            elif rds_info["Category"] == "Finance":
                rds_info["Category"] = "金融版"
            else:
                pass
            if rds_info["PayType"] == "Postpaid":
                rds_info["PayType"] = "按量付费"
            elif rds_info["PayType"] == "Prepaid":
                rds_info["PayType"] = "包年包月"
            else:
                pass
            if rds_info["DBInstanceClassType"] == "s":
                rds_info["DBInstanceClassType"] = "共享型"
            elif rds_info["DBInstanceClassType"] == "x":
                rds_info["DBInstanceClassType"] = "通用型"
            elif rds_info["DBInstanceClassType"] == "d":
                rds_info["DBInstanceClassType"] = "独享套餐"
            elif rds_info["DBInstanceClassType"] == "h":
                rds_info["DBInstanceClassType"] = "独占物理机"
            else:
                pass
            if rds_info["DBInstanceStatus"] == "Creating":
                rds_info["DBInstanceStatus"] = "创建中"
            elif rds_info["DBInstanceStatus"] == "Running":
                rds_info["DBInstanceStatus"] = "运行中"
            elif rds_info["DBInstanceStatus"] == "Deleting":
                rds_info["DBInstanceStatus"] = "删除中"
            elif rds_info["DBInstanceStatus"] == "Rebooting":
                rds_info["DBInstanceStatus"] = "重启中"
            elif rds_info["DBInstanceStatus"] == "DBInstanceClassChanging	":
                rds_info["DBInstanceStatus"] = "升降级中"
            elif rds_info["DBInstanceStatus"] == "TRANSING":
                rds_info["DBInstanceStatus"] = "迁移中"
            elif rds_info["DBInstanceStatus"] == "EngineVersionUpgrading":
                rds_info["DBInstanceStatus"] = "迁移版本中"
            elif rds_info["DBInstanceStatus"] == "TransingToOthers":
                rds_info["DBInstanceStatus"] = "迁移数据到其他RDS中"
            elif rds_info["DBInstanceStatus"] == "GuardDBInstanceCreating":
                rds_info["DBInstanceStatus"] = "生产灾备实例中"
            elif rds_info["DBInstanceStatus"] == "Restoring":
                rds_info["DBInstanceStatus"] = "备份恢复中"
            elif rds_info["DBInstanceStatus"] == "Importing":
                rds_info["DBInstanceStatus"] = "数据导入中"
            elif rds_info["DBInstanceStatus"] == "ImportingFromOthers":
                rds_info["DBInstanceStatus"] = "从其他RDS实例导入数据中"
            elif rds_info["DBInstanceStatus"] == "DBInstanceNetTypeChanging	":
                rds_info["DBInstanceStatus"] = "内外网切换中"
            elif rds_info["DBInstanceStatus"] == "GuardSwitching":
                rds_info["DBInstanceStatus"] = "容灾切换中"
            elif rds_info["DBInstanceStatus"] == "INS_CLONING":
                rds_info["DBInstanceStatus"] = "实例克隆中"
            else:
                rds_info["DBInstanceStatus"] = "未识别的状态"

            rds_info["DBInstanceDiskUsed"] = rds_info["DBInstanceDiskUsed"]/1024/1024/1024
            local_time = str(othHandler.utc2local("%Y-%m-%dT%H:%M:%SZ",rds_info["CreationTime"]))
            rds_info["CreationTime"] = local_time
            time_list = rds_info["MaintainTime"].split("-")
            local_maintain_time_list = []
            for tm in time_list:
                ti = str(othHandler.utc2local("%H:%MZ",tm).time())

                local_maintain_time_list.append(ti)
            local_maintain_time = "--".join(local_maintain_time_list)
            rds_info["MaintainTime"] = local_maintain_time
            print(rds_info)
        return render(request,"aliyun/rds/info.html",locals())

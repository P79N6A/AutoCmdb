#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: dns.py
@time: 2018/11/15 10:49
@desc:
'''
import json
from aliyun.service import aliHandle
from django.views import View
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from aliyun.models import AliAccount,Region
from aliyun.forms import ali_account_form
from aliyun.Forms import detailDns
from django.contrib.auth.decorators import login_required
from aliyun.service.othHandler import ali_rbac
from django.db.models import F, Q
from django.shortcuts import render,HttpResponse,redirect
from rbac.models import User2Role,Permission2Action2Role
from rbac.cbv.views import RbacView


class dnsListViews(View):
    """
        查看阿里dns记录列表
        """
    def get(self, request, *args, **kwargs):
        allAct = AliAccount.objects.values("accountName")
        return render(request, 'aliyun/domain/index.html', locals())


class DnsRecords(View):
    """
    获取阿里解析记录API
    """

    def post(self, request, *args, **kwargs):
        dic_news = {
            "state": 0,
            "code": 0
            , "msg": ""
            , "count": 3000000
            , "data": []}

        accountName = request.POST.get("accountName")
        domainName = request.POST.get("domainName")
        PageSize = request.POST.get("pageSize")  # 当页有几列
        PageNumber = request.POST.get("pageStart")  # 当前是多少页
        RR = request.POST.get("RRKeyWord") #
        TypeKeyWord = request.POST.get("TypeKeyWord")
        ValueKeyWord = request.POST.get("ValueKeyWord")
        allAct = AliAccount.objects.values("accessKey", "accessSecret").filter(accountName=accountName).first()
        dns = aliHandle.AliyunDns(allAct["accessKey"], allAct["accessSecret"])
        dict_dns = dns.get_domain_records(DomainName=domainName,PageSize=PageSize,PageNumber=PageNumber,RRKeyWord=RR,
                                          TypeKeyWord=TypeKeyWord,ValueKeyWord=ValueKeyWord)


        count = dict_dns["TotalCount"]
        dic_news["count"] = count
        dnsRecordsList = dict_dns["DomainRecords"]["Record"]
        if dnsRecordsList:
            dic_news["state"] = 0
            for record in dnsRecordsList:
                if "Priority" not in record.keys():
                    record["Priority"] = "--"
                if record["Line"] == "default":
                    record["line"] = "默认"
                if record["Status"] == "ENABLE":
                    record["Status"] = "<span style='color:green' class='statgg' id={}>正常</span>".format(record["RecordId"])
                else:
                    record["Status"] = "<span style='color:red' class='statgg'>暂停</span>".format(record["RecordId"])
                record["TTL"] = "{}分钟".format(record.get("TTL") // 60)
                dic_news["data"].append(record)
        else:
            dic_news["state"] = 1
        return JsonResponse(dic_news)


class dnsRecordSetStatus(View):

    def post(self, request, *args, **kwargs):
        accountName = request.POST.get("accountName")
        RecordId = request.POST.get("RecordId")
        event = request.POST.get("event")
        print(RecordId)

        allAct = AliAccount.objects.values("accessKey", "accessSecret").filter(accountName=accountName).first()
        dns = aliHandle.AliyunDns(allAct["accessKey"], allAct["accessSecret"])
        code = dns.get_dns_status(RecordId)["Status"]
        print(code)
        if code == "ENABLE":
            status = "DISABLE"
        else:
            status = "ENABLE"
        result = dns.set_dns_status(RecordId, status)
        print(result)
        return JsonResponse(result)


class dnsRecordDelete(View):

    def post(self, request, *args, **kwargs):
        accountName = request.POST.get("accountName")
        RecordId = request.POST.get("RecordId")
        event = request.POST.get("event")
        print(RecordId)
        allAct = AliAccount.objects.values("accessKey", "accessSecret").filter(accountName=accountName).first()
        dns = aliHandle.AliyunDns(allAct["accessKey"], allAct["accessSecret"])
        code = dns.get_dns_status(RecordId)["Status"]
        print(code)
        if code == "ENABLE":
            status = "DISABLE"
        else:
            status = "ENABLE"
        result = dns.set_dns_status(RecordId, status)
        print(result)
        return JsonResponse(result)


class DnsRecordsViews(View):

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
        domainName = request.GET.get("domainName")
        return render(request,"aliyun/dns/records.html",locals())


class DnsRecordsTest(View):

    def get(self, request, *args, **kwargs):
        accountName = request.GET.get("accountName")
        domainName = request.GET.get("domainName")
        return redirect("dns_records",locals())


class dnsViews(View):
    """
        查看阿里dns记录
        """

    def get(self, request, *args, **kwargs):
        accountName = request.GET.get("accountName")
        domainName = request.GET.get("domainName")
        allAct = AliAccount.objects.values("accessKey", "accessSecret").filter(accountName=accountName).first()
        dns = aliHandle.AliyunDns(allAct["accessKey"],allAct["accessSecret"])
        result = dns.get_domain_records(DomainName=domainName)
        return render(request, 'aliyun/domain/index.html', locals())


class detailDnsRecord(View):

    def get(self, request, *args, **kwargs):
        accountName = request.GET.get("accountName")
        RecordId = request.GET.get("RecordId")
        domainName = request.GET.get("domainName")
        RR = request.GET.get("RR")

        allAct = AliAccount.objects.values("accessKey", "accessSecret").filter(accountName=accountName).first()
        dns = aliHandle.AliyunDns(allAct["accessKey"], allAct["accessSecret"])
        result = dns.get_domain_records(DomainName=domainName,RRKeyWord=RR)
        for z in result["DomainRecords"]["Record"]:
            if z["DomainName"] == domainName:
                record = z
                print(record)
            else:
                record = False
        form = detailDns.detailDnsRecordsForm()
        return render(request, "aliyun/dns/detail_dns_record.html",locals())

    def post(self, request, *args, **kwargs):

        # accountName = request.GET.get("accountName")
        # # RecordId = request.GET.get("RecordId")
        # domainName = request.GET.get("domainName")
        # RR = request.GET.get("RR")
        # allAct = AliAccount.objects.values("accessKey", "accessSecret").filter(accountName=accountName).first()
        # dns = aliHandle.AliyunDns(allAct["accessKey"], allAct["accessSecret"])
        # result = dns.get_domain_records(DomainName=domainName, RRKeyWord=RR)
        Type = request.POST.get("all_obj[remarkType]")

        RR = request.POST.get("all_obj[domainType]")
        line = request.POST.get("all_obj[line]")
        mx = request.POST.get("all_obj[mx]")
        ttl = request.POST.get("all_obj[ttl]")
        value = request.POST.get("all_obj[value]")
        domainName = request.POST.get("domainName")
        accountName = request.POST.get("accountName")
        RecordId = request.POST.get("RecordId")
        allAct = AliAccount.objects.values("accessKey", "accessSecret").filter(accountName=accountName).first()
        dns = aliHandle.AliyunDns(allAct["accessKey"], allAct["accessSecret"])
        print(RR,Type,line,mx,ttl,value,RecordId,)
        result = dns.set_domain_records(RecordId=RecordId,RR=RR,Type=Type,Value=value,TTL=ttl,Priority=mx,Line=line)
        print(result)
        return JsonResponse({"state":0})


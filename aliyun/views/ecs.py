#!/usr/bin/env python
# encoding: utf-8
import json
from django.views import View
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from aliyun.models import AliAccount, Region, AliEcs
from aliyun.forms import ali_account_form, ali_account_region_form
from django.contrib.auth.decorators import login_required
from rbac.cbv.views import RbacView
from rbac.models import User, Role, User2Role, Menu, Permission, Action, Permission2Action2Role
from django.db.models import F, Q
from aliyun.service.othHandler import ali_rbac
import logging
# 生成一个logger实例，专门用来记录日志
logger = logging.getLogger(__name__)



class aliViews(RbacView, View):

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

        return render(request, 'aliyun/basic/index.html', locals())


class ecsViews(RbacView, View):
    """
    查看阿里ECS资源
    """

    @ali_rbac(url="aliyun/ecs/ecs.html")
    def get(self, request, *args, **kwargs):
        allAct = AliAccount.objects.values("accountName")
        logger.error(allAct)
        return render(request, 'aliyun/ecs/ecs.html', locals())


class getAccount(RbacView, View):
    """
    二级联动，获取账号
    """

    def post(self, request, *args, **kwargs):
        data = AliAccount.objects.values("id", "accountName").all()
        print(data)
        return HttpResponse(json.dumps(list(data)))


class getActRegion(RbacView, View):
    """
    二级联动，获取可用区
    """

    def post(self, request, *args, **kwargs):
        prov_selected = request.POST.get("prov_selected")
        print(prov_selected)
        data = Region.objects.filter(aliaccount__id=prov_selected).values("RegionId", "RegionName").all()
        print(data)
        return HttpResponse(json.dumps(list(data)))


class aliAccountRegion(RbacView, View):

    def post(self, request, *args, **kwargs):
        import json
        data = request.POST
        act = data.get("act", None)
        print(data)
        act_objs = 0
        if act:
            act_obj = list(Region.objects.filter(aliaccount__accountName=act).values("RegionName", "RegionId"))
            act_objs = json.dumps(act_obj)
            print(act_objs)
        return HttpResponse(act_objs)


class aliAccountRegionS(RbacView, View):

    def post(self, request, *args, **kwargs):
        print(1)
        n_form = ali_account_region_form(request.POST)
        print(n_form)
        return render(request, "aliyun/ecs/ecs.html", locals())


class getEcsView(RbacView, View):
    """
    获取ecs
    """

    def post(self, request, *args, **kwargs):
        """
        :param request:
            suppUserId
            suppId
        :param args:
        :param kwargs:
        :return:
        """
        suppUserId = request.POST.get("suppUserId")
        suppId = request.POST.get("suppId")
        print(suppUserId, suppId)
        if suppUserId == "请选择":
            pass
        if suppId == "请选择":
            pass
        if suppUserId == "所有账号":
            pass
        dic_new = {"code": 0
            , "msg": ""
            , "count": 3000000
            , "data": []}
        import json
        from aliyun import models

        ali_account_list = []
        ali_account_all = list(AliAccount.objects.values("accountName").all())
        for ali_account in ali_account_all:
            ali_account_list.append(ali_account["accountName"])
        print(ali_account_all)
        if suppUserId == "全部" and suppId == "1":
            objs = models.AliEcs.objects.values("id", "ImageId", "InstanceTypeFamily", "ZoneId", "Memory", "Cpu",
                                                "StartTime",
                                                "InstanceName", "ExpiredTime", "PublicIpAddress_IpAddress",
                                                "VpcAttributes_PrivateIpAddress_IpAddress", "OSName",
                                                "account__accountName").all()
        elif suppUserId in ali_account_list and suppUserId != "全部" and suppId == "1":
            objs = models.AliEcs.objects.values("id", "ImageId", "InstanceTypeFamily", "ZoneId", "Memory", "Cpu",
                                                "StartTime",
                                                "InstanceName", "ExpiredTime", "PublicIpAddress_IpAddress",
                                                "VpcAttributes_PrivateIpAddress_IpAddress", "OSName",
                                                "account__accountName").filter(account__accountName=suppUserId).all()
        else:
            objs = models.AliEcs.objects.values("id", "ImageId", "InstanceTypeFamily", "ZoneId", "Memory", "Cpu",
                                                "StartTime",
                                                "InstanceName", "ExpiredTime", "PublicIpAddress_IpAddress",
                                                "VpcAttributes_PrivateIpAddress_IpAddress", "OSName",
                                                "account__accountName").filter(account__accountName=suppUserId,
                                                                               RegionId__RegionId=suppId).all()

        for i in objs:
            for key, value in i.items():

                if type(value) == str:
                    if "[" in value:
                        print(value, 1111)
                        i.update({key: value[2:-2]})
                        # print(value)

            dic_new.get("data").append(i)

        from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
        limit = request.POST.get("pageSize")  # 当页有几列
        page = request.POST.get("pageStart")  # 当前是多少页
        paginator = Paginator(dic_new["data"], limit)
        count = len(dic_new["data"])
        currentPage = int(page)
        dic_new["data"] = paginator.page(page).object_list
        dic_new["count"] = count
        print(dic_new)
        s = json.dumps(dic_new)

        return JsonResponse(dic_new, content_type="application/json, charset=utf-8")

    def get(self, request, *args, **kwargs):

        pass


class updateEcsView(RbacView, View):
    """ECS获取并入库"""

    def edit(self, request, *args, **kwargs):
        """
        :param request:
            suppUserId
            suppId
        :param args:
        :param kwargs:
        :return:
        """
        suppUserId = request.POST.get("suppUserId")
        suppId = request.POST.get("suppId")
        code = 0
        print(suppUserId, suppId, 1)
        if suppUserId == "请选择":
            pass
        if suppId == "请选择":
            pass
        if suppUserId == "所有账号":
            pass

        else:
            print(suppUserId, suppId, 2)
            account_id = AliAccount.objects.values("id").filter(accountName=suppUserId).first().get("id")
            print(account_id)
            ali_ac = AliAccount.objects.filter(accountName=suppUserId).values("accessKey", "accessSecret").first()
            print(ali_ac)
            accessKey = ali_ac.get("accessKey")
            accessSecret = ali_ac.get("accessSecret")
            from aliyun.service import aliHandle
            ali_obj = aliHandle.AliyunEcs(accessKey=accessKey, accessSecret=accessSecret, region=suppId,
                                          account=account_id)
            ali_ecs_data = ali_obj.insert_db()
            code = 1
            print(ali_ecs_data)
        return HttpResponse(code)


class deleteEcs(RbacView, View):

    def delete(self, request, *args, **kwargs):
        ecs_id = request.POST.get("uvid")
        print(ecs_id)
        try:
            ali_ecs_obj = AliEcs.objects.filter(id=ecs_id).first()
            if ali_ecs_obj:
                ali_ecs_obj.delete()
            state = {"state": 1}
        except Exception as e:
            state = {"state": 0}
        return JsonResponse(state)


class getEcsInfo(RbacView,View):

    def post(self, request, *args, **kwargs):
        ecs_id = request.POST.get("uvid")
        print(ecs_id)
        try:
            ali_ecs_obj = AliEcs.objects.values().filter(id=ecs_id).first()
            exclude_fields = ('user', 'add_time')
            params = [f for f in AliEcs._meta.fields if f.name not in exclude_fields]
            field_dic = {}

            for msg in params:
                field_dic[msg.name] = msg.verbose_name
            # for field in modelobj._meta.fields:
            #     field_dic[field.name] = field.verbose_name

            ali_ecs_obj_dic = {}

            for key, value in ali_ecs_obj.items():
                ali_ecs_obj_dic[field_dic.get(key)] = value
            print(1, ali_ecs_obj_dic)
            if ali_ecs_obj:
                state = {"state": 1, "ecs_info": ali_ecs_obj}
        except Exception as e:
            print(e)
            state = {"state": 0, }
        print(2)
        return JsonResponse(state)


class getEcsInfoView(RbacView,View):

    def get(self, request, *args, **kwargs):
        print(args, kwargs, request.GET.get("uid"))
        return render(request, "aliyun/ecs/ecs_info.html", locals())

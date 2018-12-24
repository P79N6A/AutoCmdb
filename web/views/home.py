#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render,redirect
from django.http import JsonResponse
from web.service import chart
from rbac.cbv.views import RbacView
from rbac.models import User,Role,User2Role,Menu,Permission,Action,Permission2Action2Role
from django.db.models import F, Q
from django.contrib.auth.decorators import login_required


class IndexView(RbacView,View):

    def get(self, request, *args, **kwargs):
        state = request.GET.get("state")
        print(request.session.get('user_info'))
        print(request.session.__dict__)
        rbac_menu_permission = request.session.get("rbac_permission_session_key")
        username = request.session.get("user_info").get("username")
        print(username)
        role_caption = User2Role.objects.values("role__caption").filter(user__username=username).first()
        print(role_caption)
        rbac_list = list(Permission2Action2Role.objects.values("permission__menu", "action__code", "permission__url",
                                                               "permission__caption", "permission__menu__caption",
                                                               "permission__menu__parent").filter(
            Q(permission__url__in=rbac_menu_permission.keys()) & Q(role__caption=role_caption["role__caption"])))

        for i in rbac_list:
            i["permission__url"] = i["permission__url"].split("$")[0]
        print(request.session.get('user_info'))
        if not request.session.get('user_info'):
            return redirect('/login/')
        return render(request, 'index.html',locals())


class CmdbView(RbacView,View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cmdb.html')


class ChartView(View):
    def get(self, request, chart_type):
        if chart_type == 'business':
            response = chart.Business.chart()
        if chart_type == 'dynamic':
            last_id = request.GET.get('last_id')
            response = chart.Dynamic.chart(last_id)
        return JsonResponse(response.__dict__, safe=False, json_dumps_params={'ensure_ascii': False})

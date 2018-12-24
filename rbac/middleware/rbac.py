#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,render,redirect
from repository.models import UserProfile

class RbacMiddleware(MiddlewareMixin):
    def process_request(self, request, *args, **kwargs):
        """
        检查用户是否具有权限访问当前URL
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """

        """跳过无需权限访问的URL"""

        for pattern in settings.RBAC_NO_AUTH_URL:
            if re.match(pattern, request.path_info):
                return None

        """获取当前用户session中的权限信息"""
        permission_dict = request.session.get(settings.RBAC_PERMISSION_SESSION_KEY)
        if not permission_dict:

            return redirect('/login/')

        session_id = request.session.__dict__["_SessionBase__session_key"]
        print(444444444,session_id)
        UserProfile.objects.filter(user__username=request.session["user"]).update(session=session_id)
        # import datetime
        # lastLoginDate = request.session["user_info"]["lastLoginDate"]
        # print(111,request.session.__dict__)
        # user = UserProfile.objects.get(user__username=request.session["user_info"]["username"])
        # if lastLoginDate != user.last_login_date:
        #     return render(request, 'login.html', {'msg': '已在别地登陆，禁止访问'})

        """当前URL和session中的权限进行匹配"""

        flag = False
        print(request.POST)
        for pattern, code_list in permission_dict.items():
            upper_code_list = [item.upper() for item in code_list]

            if re.match(pattern, request.path_info):
                request_permission_code = request.session.get(settings.RBAC_QUERY_KEY, code_list[0]).upper()
                if request_permission_code in upper_code_list:
                    request.permission_code = request_permission_code
                    request.permission_code_list = upper_code_list
                    flag = True
                    break
        if not flag:
            return redirect('/login/')
            # return redirect(request, "/login/", settings.RBAC_PERMISSION_MSG)

#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import datetime,time
from django.views import View
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect ,HttpResponse, get_object_or_404,reverse
from web.service import chart
from rbac.service import initial_permission
from rbac.cbv.views import RbacView
from repository.models import UserProfile
from rbac.models import User
from django.utils.timezone import utc
from django_redis import get_redis_connection
from django.core.cache import cache
from geetest.geetest import GeetestLib

class BasePagPermission(object):
    def __init__(self, code_list):
        self.code_list = code_list

    def has_add(self):
        if "add" in self.code_list:
            return True

    def has_del(self):
        if "del" in self.code_list:
            return True

    def has_edit(self):
        if "edit" in self.code_list:
            return True


class BaseView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "base.html")

    def post(self, request, *args, **kwargs):
        pass



class TestView(View):
    def get(self, request, *args, **kwargs):

        dic_new = {"code": 0
                   ,"msg": ""
                   ,"count": 3000000
                   ,"data":[]}
        import json
        from aliyun import models
        objs = models.AliEcs.objects.values("id","ImageId","InstanceTypeFamily","ZoneId","Memory","Cpu","StartTime",
                                            "InstanceName","ExpiredTime").all()
        for i in objs:

            dic_new.get("data").append(i)

        s = json.dumps(dic_new)


        return JsonResponse(dic_new,content_type="application/json, charset=utf-8")


    def post(self, request, *args, **kwargs):
        pass


# 极验验证,请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "e947824a415ddfdce30e5ff3e91e8086"  # id
pc_geetest_key = "47c642acc5dff090bbb1be5763a92ece"  # key

def pcgetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    print(response_str)
    return HttpResponse(response_str)


def acc_login(request):
    error = ""
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        next = request.META.get('HTTP_REFERER')
        print(next)
        username = request.POST.get("username")
        password = request.POST.get("password")
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        print(request.session.__dict__,555)
        status = request.session[gt.GT_STATUS_SESSION_KEY]

        user_id = request.session["user_id"]
        user_list = []
        try:
            conn = get_redis_connection("default")
            user = UserProfile.objects.filter(user__username=username).first()
            if not user:
                return render(request, 'login.html', {'msg': '未查询到此账号!'})
            if int(user.login_state):
                print(type(bool(user.login_state)),bool(user.login_state),user.login_state)
                return render(request, 'login.html', {'msg': '账号已经冻结!'})
            if (datetime.datetime.now() - user.login_lock_date).total_seconds() < 600:
                return render(request, 'login.html', {'msg': '账号锁定十分钟内不能登陆!'})
            if user.pass_err_count >= 3:
                user.login_lock_date = datetime.datetime.now()
                user.save()
                return render(request, 'login.html', {'msg': '密码输入超过5次，用户锁定十分钟'})

            obj = UserProfile.objects.filter(user__username=username, user__password=password).first()
            if status:
                result = gt.success_validate(challenge, validate, seccode, user_id)
            else:
                result = gt.failback_validate(challenge, validate, seccode)

            print(555555555,result)
            if result:
                if obj:
                    pduser = UserProfile.objects.values("session").filter(user__username=username)[0]
                    print(111,type(pduser["session"]))
                    # 如果session为“None”则说明还没有登录过的新用户
                    if pduser["session"] == None:
                        request.session["user"] = username
                        request.session['user_info'] = {'username': username, 'nickname': obj.nickname, 'nid': obj.user.id,}
                        initial_permission(request, obj.user.id)
                        session_id = request.session.__dict__["_SessionBase__session_key"]
                        print(444444444, session_id)
                        return redirect(request.GET.get("next") or "/index.html", locals())
                    else:
                        print(request.session.__dict__)
                        print(pduser)
                        request.session.delete(pduser["session"])

                        request.session["user"] = username
                        request.session['user_info'] = {'username': username, 'nickname': obj.nickname,
                                                        'nid': obj.user.id, }
                        session_id = request.session.__dict__["_SessionBase__session_key"]
                        # print(session_id)
                        # UserProfile.objects.filter(user__username=username).update(session=session_id)
                        initial_permission(request, obj.user.id)
                        return redirect(request.GET.get("next") or "/index.html", locals())
                else:
                    error = "Wrong username or password !"
                    user.pass_err_count += 1
                    user.save()
                    return render(request, "login.html", {"error": error})
            else:
                ret["status"] = 1
                ret["msg"] = "验证码错误"
            return JsonResponse(ret)
        except Exception as e:
            print(e)
            return render(request, "login.html", {"msg": e})

    return render(request, "login.html",{"error":error})


# class LoginView(View):
#     def get(self, request, *args, **kwargs):
#         pass


def acc_logout(request):
    username = request.GET.get("username")
    print(username)
    user = UserProfile.objects.filter(nickname=username).update(isNot_login=False)
    print(user)
    logout(request)
    return redirect("/login/")




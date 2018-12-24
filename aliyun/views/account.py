#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: account.py
@time: 2018/11/9 16:32
@desc:
'''
import json
from django.views import View
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from aliyun.models import AliAccount,Region
from aliyun.forms import ali_account_form
from django.contrib.auth.decorators import login_required




def get_act(accountName):
    """
    {"state": 0, "msg": ""}
    1 成功    0 失败
    :param accountName:
    :return:
    """
    Act = {"state": 0, "msg":""}
    try:
        allAct = AliAccount.objects.values("accessKey", "accessSecret").filter(accountName=accountName).first()
        Act.update(allAct)
        Act["state"] = 1
    except Exception as e:
        print(e)
        Act["msg"] = e
    return Act


class aliAccount(View):
    """
    查看阿里账号
    """
    def get(self, request, *args, **kwargs):
        allAct = AliAccount.objects.all()
        display_control = "none"
        n_form = ali_account_form()
        # print(n_form)
        return render(request,"aliyun/account/index.html",locals())


class aliAccountAdd(View):
    """
    ali accesssKey 账号增加
    """
    def post(self, request, *args, **kwargs):
        n_form = ali_account_form(request.POST)
        if n_form.is_valid():
            n_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render(request, "aliyun/account/add.html", locals())


    def get(self, request, *args, **kwargs):
        display_control = "none"
        n_form = ali_account_form()
        return render(request, "aliyun/account/add.html", locals())


class aliAccountDel(View):
    """
    ali accesssKey 账号删除
    """


    def post(self, request, *args, **kwargs):

        data = request.POST
        print(data)
        env_items = request.POST.getlist('id_list[]')
        if env_items:
            for n in env_items:
                AliAccount.objects.filter(id=n).delete()
        all_env = AliAccount.objects.all()
        return render(request, "aliyun/account/index.html", locals())


class aliAccountEdit(View):
    """
    ali accesssKey 账号删除
    """

    def get(self, request, *args, **kwargs):
        id = request.GET.get("id")
        print(id)
        status = 2
        all_act = AliAccount.objects.filter(id=id).all()
        return render(request, "aliyun/account/update.html", locals())


    def post(self,request, *args, **kwargs):
        status = 1
        env_url = "123"
        all_env = AliAccount.objects.all()

        mu_url = request.POST.getlist('mu_url')
        for url_id in mu_url:
            url_list.append(EnvironUrl.objects.get(id=url_id).url)
        wai_id = request.POST.get("wai")
        nei_id = request.POST.get("nei")
        wai_item = Environ.objects.get(id=wai_id)
        wai_ex = wai_item.ex
        nei_item = Environ.objects.get(id=nei_id)
        nei_ex = nei_item.ex
        for url in url_list:
            url = url + "sets/set"
            print(url)
            ui_status = get_request(url, **{"w": wai_ex, "n": nei_ex})
            print(ui_status.text)
        return render(request, "aliyun/account/update.html", locals())
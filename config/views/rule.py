#!/usr/bin/env python
# encoding: utf-8
"""
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: role.py
@time: 2018/12/7 11:38
@desc:
"""
import json
from django.views import View
from django.shortcuts import render, HttpResponse, redirect
from rbac.cbv.views import RbacView



class ruleView(View):
    def get(self,request):
        return HttpResponse("ok")
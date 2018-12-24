#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: rbacForm.py
@time: 2018/12/10 14:31
@desc:
'''

from django.forms import  Form,widgets  ##Form要继承的
from django.forms import ModelForm  ##ModelForm继承
from  rbac import models


class menuAddForm(ModelForm):
    class Meta:
        model = models.Menu  ##里面必须要有一个model，因为他是对每个models类做增删改查的
        fields =  "__all__"  ##指定了类，要需要指定要处理哪几个字段 __all__是全部字段
        widgets = {
            "caption":widgets.TextInput(attrs={"class":"layui-input"}),
            "level": widgets.TextInput(attrs={"class": "layui-input","id":"level"})
        }

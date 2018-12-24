#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: Forms.py
@time: 2018/11/8 10:29
@desc:
'''

from django import forms
from .models import AliAccount


class ali_account_form(forms.ModelForm):

    def clean(self):
        cleaned_data = super(ali_account_form, self).clean()
        value = cleaned_data.get("accountName")
        try:
            AliAccount.objects.get(accountName=value)
            self.add_error("accountName","%s的信息已经存在" % value)

        except AliAccount.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = AliAccount
        fields = ["accountName","accessKey","accessSecret","region"]
        from django.forms import widgets as wid
        widgets = {
            "region":wid.SelectMultiple(attrs={"id":"my-select","multiple":"multiple",}),
            "accountName":wid.Input(attrs={"lay-verify":"required","placeholder":"请输入","autocomplete":"off","class":"layui-input"}),
            "accessSecret": wid.Input(
                attrs={"lay-verify": "required", "placeholder": "请输入", "autocomplete": "off", "class": "layui-input"}),
            "accessKey": wid.Input(
                attrs={"lay-verify": "required", "placeholder": "请输入", "autocomplete": "off", "class": "layui-input"})
        }
        exclude = ("id",)

provinces = AliAccount.objects.all()
PROVINCE_CHOICES = []
for province in provinces:

    PROVINCE_CHOICES.append([province.id, province.accountName])


class ali_account_region_form(forms.ModelForm):
    province = forms.ChoiceField(widget = forms.Select(attrs={'class':'select'}), choices = PROVINCE_CHOICES, label= u'选择省')
    city = forms.ChoiceField(widget = forms.Select(attrs={'class':'select'}), label = u'选择市')
    #如果需要3级联动，在city中也添加onChange参数指定就jquery函数

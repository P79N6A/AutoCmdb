#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: detailDns.py
@time: 2018/11/15 16:24
@desc:
'''
from django.forms import Form
from django.forms import widgets
from django.forms import fields


class detailDnsRecordsForm(Form):
    remarkType = fields.CharField(
        initial=1,
        widget=widgets.Select(choices=(("A","A- 将域名指向一个IPV4地址"),
                                       ("CNAME","CNAME- 将域名指向另外一个域名"),
                                       ("AAAA","AAAA- 将域名指向一个IPV6地址"),
                                       ("NS","NS- 将子域名指定其他DNS服务器解析"),
                                       ("MX","MX- 将域名指向邮件服务器地址"),
                                       ("SRV","SRV- 记录提供特定的服务的服务器"),
                                       ("TXT", "TXT- 文本长度限制512，通常做SPF记录（反垃圾邮件）"),
                                       ("CAA", "CAA- CA证书颁发机构授权校验"),
                                       ("REDIRECT_URL", "显性URL- 将域名302重定向到另外一个地址"),
                                       ("FORWARD_URL", "隐形URL- 与显性URL类似，但是会隐藏真实目标地址"),
                                       ),attrs={"lay-verify":"test","id":"remarkType"},)
    )

    domainType = fields.CharField(
        widget=widgets.TextInput(attrs={'id': 'domainType', 'class': 'layui-input'})
    )

    line = fields.CharField(
        initial=1,
        widget=widgets.Select(choices=(("default", "默认-必填！未匹配到智能解析线路时，返回【默认】线路设置结果"),
                                       ("unicom", "中国联通"),
                                       ("telecom", "中国电信"),
                                       ("mobile", "中国移动"),
                                       ("edu", "中国教育网"),
                                       ("oversea", "境外-向除中国大陆以外的其他国家和地区，返回设置的记录值"),
                                       ("baidu", "百度"),
                                       ("biying", "必应"),
                                       ("google", "谷歌"),
                                       ),attrs={"id":"Line","class":"lllll"})
    )
    value = fields.CharField(
        required=False,
        widget=widgets.TextInput(attrs={'id': 'value', 'class': 'layui-input',"layui-filter":"domainvalut","value":"1"})
    )

    mx = fields.CharField(
        required=True,
        widget=widgets.TextInput(attrs={ 'class': 'layui-input'})
    )
    ttl = fields.CharField(
        initial=1,
        widget=widgets.Select(choices=((600, "10分钟"),
                                       (1800, "30分钟"),
                                       (3600, "1小时"),
                                       (43200, "12小时"),
                                       (86400, "1天"),
                                       ),attrs={'id': 'ttl'})
    )







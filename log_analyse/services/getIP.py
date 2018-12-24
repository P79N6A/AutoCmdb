#!/usr/bin/env python
# encoding: utf-8
'''
@author: jerry
@contact: wangqiyuan@blhcn.com
@file: getIP.py
@time: 2018/12/14 22:34
@desc:
'''
import os,json,requests
import geoip2.database
import sys,socket,struct
import time
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoCmdb.settings")
django.setup()
from log_analyse.models import IpInfo,NginxLog

from log_analyse.services.redis_queue import RedisQueue
from log_analyse.services.logger import MyLogger
start_time = time.time()
dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
reader = geoip2.database.Reader(dir_path+"\db\GeoLite2-City.mmdb")


def get_ip(ip):
    """基于GEOip"""
    ip_info = {}

    data = reader.city(ip)
    ip_info["ip"] = ip
    ip_info["Country"] = data.country.names.get("zh-CN")
    ip_info["Subdivisions"] = data.subdivisions.most_specific.names.get("zh-CN")
    ip_info["City"] = data.city.names.get("zh-CN")
    ip_info["Latitude"] = data.location.latitude
    ip_info["Longitude"] = data.location.longitude
    return ip_info

def get_ip_v2(ip):
    """基于阿里云api"""
    host = 'http://ipquery.market.alicloudapi.com'
    path = '/query'
    method = 'GET'
    appcode = '1ba6f6e6fa3844d8b557887948d77c50'
    querys = 'ip={}'.format(ip)
    bodys = {}

    new_data = {}
    url = host + path + '?' + querys
    with requests.Session() as s:
        msg = s.get(url, headers={"Authorization": 'APPCODE ' + appcode})
    msg = msg.json()
    if msg["ret"] == 200:
        new_data["Country"] = msg["data"].get("country")
        new_data["country_code"] = msg["data"].get("country_code")
        new_data["Subdivisions"] = msg["data"].get("prov")
        new_data["City"] = msg["data"].get("city")
        new_data["city_code"] = msg["data"].get("city_code")
        new_data["city_short_code"] = msg["data"].get("city_short_code")
        new_data["Area"] = msg["data"].get("area")
        # new_data["post_code"] = msg["data"]["post_code"]
        new_data["area_code"] = msg["data"].get("area_code")
        new_data["Isp"] = msg["data"].get("isp")
        new_data["Longitude"] = msg["data"].get("lng")
        new_data["Latitude"] = msg["data"].get("lat")
        new_data["ip"] = socket.inet_ntoa(struct.pack('!L', msg["data"].get("long_ip")))
        new_data["big_area"] = msg["data"].get("big_area")
    return new_data

def get_ip_v3(ip):
    """
    基于
    :param ip:
    :return:
    """
    host = 'http://whois.pconline.com.cn'
    path = '/ipJson.jsp'
    method = "GET"
    querys = 'ip={}&json=true'.format(ip)
    url = host + path + "?" + querys

    new_data = {}
    msg = requests.get(url)
    msg = msg.json()
    if msg["ret"] == 200:
        new_data["Country"] = msg["data"].get("country")
        new_data["country_code"] = msg["data"].get("country_code")
        new_data["Subdivisions"] = msg["data"].get("prov")
        new_data["City"] = msg["data"].get("city")
        new_data["city_code"] = msg["data"].get("city_code")
        new_data["city_short_code"] = msg["data"].get("city_short_code")
        new_data["Area"] = msg["data"].get("area")
        # new_data["post_code"] = msg["data"]["post_code"]
        new_data["area_code"] = msg["data"].get("area_code")
        new_data["Isp"] = msg["data"].get("isp")
        new_data["Longitude"] = msg["data"].get("lng")
        new_data["Latitude"] = msg["data"].get("lat")
        new_data["ip"] = socket.inet_ntoa(struct.pack('!L', msg["data"].get("long_ip")))
        new_data["big_area"] = msg["data"].get("big_area")
    return new_data

def test(chuck):
    log_dict = json.loads(chuck)
    ip = get_ip(log_dict["true_ip"])
    ip_obj = IpInfo.objects.values("id", "ip").filter(ip=ip["ip"]).first()
    if not ip_obj:
        try:
            z = IpInfo(**ip)
            z.save()
        except Exception as e:
            print(e)

    log_ip = IpInfo.objects.values("id").filter(ip=log_dict["true_ip"]).first()

    log_dict.pop("true_ip")
    log_dict["true_ip_id"] = log_ip["id"]
    format1 = '%Y-%m-%dT%H:%M:%S+08:00'
    format2 = '%Y-%m-%d %H:%M:%S'
    t1 = log_dict["log_time"]
    t = time.strptime(t1,format1)
    t2 = time.strftime(format2,t)
    log_dict["log_time"] = t2
    print(log_dict)
    try:
        p=NginxLog(**log_dict)
        p.save()
    except Exception as e:
        print(e)
    # ip_list.append(ip)
    # log_list.append(log_dict)

import linecache

def get_log(filename):
    log_list = []
    ip_list = []
    z = os.path.join(dir_path,'log',filename)
    f = open(z, "rb")
    k = linecache.getlines(z)
    for chuck in k:
        d = pool.apply_async(test,args=(chuck,))
    pool.close()
    pool.join()
    return log_list,ip_list

import time

def get_update_db(key,projece_name,**redis_kwargs):
    try:
        count = 0
        logge = MyLogger()
        nginx_list = []
        q = RedisQueue(key,**redis_kwargs)
        while 1:
            if len(nginx_list) > 500:
                NginxLog.objects.bulk_create(nginx_list)
                logge.info("nginx log 入库成功")
                nginx_list = []
                continue
            result = q.get_wait(timeout=3)
            if not result:
                continue
            else:
                nginx_log_dict = json.loads(result[1])
                nginx_log_msg = nginx_log_dict["message"]
                nginx_log_msg = json.loads(nginx_log_msg)
                if nginx_log_msg["true_ip"] == "-":
                    continue

                ip_len = len(nginx_log_msg["true_ip"].split(", "))
                if ip_len > 1:
                    ip_info = nginx_log_msg["true_ip"].split(", ")[1]
                else:
                    ip_info = nginx_log_msg["true_ip"].split(", ")[0]
                ip = get_ip(ip_info)
                ip_obj = IpInfo.objects.values("id", "ip").filter(ip=ip["ip"]).first()

                if not ip_obj:
                    try:
                        o = IpInfo(**ip)

                        o.save()
                        logge.info("ip 入库成功")
                    except Exception as e:
                        print(e)
                        q.put(result)
                        logge.error("ip 入库失败")
                        continue

                try:
                    log_ip = IpInfo.objects.values("id").filter(ip=nginx_log_msg["true_ip"]).first()

                    nginx_log_msg.pop("true_ip")

                    nginx_log_msg["true_ip_id"] = log_ip["id"]
                    nginx_log_msg["projece_name"] = projece_name
                    format1 = '%Y-%m-%dT%H:%M:%S+08:00'
                    format2 = '%Y-%m-%d %H:%M:%S'
                    t1 = nginx_log_msg["log_time"]
                    t = time.strptime(t1, format1)
                    t2 = time.strftime(format2, t)
                    nginx_log_msg["log_time"] = t2
                    nginx_list.append(NginxLog(**nginx_log_msg))
                    continue
                except Exception as e:
                    print(ip_obj)
                    print(nginx_log_msg)
                    print(e)
                    logge.error("nginx log 入库失败")
                continue
    except Exception as e:
        print(e)



def get_up_db(key,projece_name,**redis_kwargs):
    count = 0
    logge = MyLogger()
    nginx_list = []
    q = RedisQueue(key,**redis_kwargs)
    start = -1000
    end = 0
    ip_len = q.qsize()
    while 1:
        if start > ip_len:
            logge.info("nginx log入库完成")
            break

        start += 1000
        end += 1000
        all_log = q.get_lrange(start, end)

        if len(nginx_list) != 0:
            NginxLog.objects.bulk_create(nginx_list)
            logge.info("nginx log 入库成功")
            nginx_list = []
            continue

        for ii in all_log:
            nginx_log_dict = json.loads(ii.decode())
            nginx_log_msg = json.loads(nginx_log_dict["message"])
            if nginx_log_msg["true_ip"] == "-":
                continue
            else:
                try:
                    log_ip = IpInfo.objects.values("id").filter(ip=nginx_log_msg["true_ip"]).first()
                    nginx_log_msg.pop("true_ip")
                    nginx_log_msg["true_ip_id"] = log_ip["id"]
                    nginx_log_msg["projece_name"] = projece_name
                    format1 = '%Y-%m-%dT%H:%M:%S+08:00'
                    format2 = '%Y-%m-%d %H:%M:%S'
                    t1 = nginx_log_msg["log_time"]
                    t = time.strptime(t1, format1)
                    t2 = time.strftime(format2, t)
                    nginx_log_msg["log_time"] = t2
                    nginx_list.append(NginxLog(**nginx_log_msg))
                    count += 1
                    print(count)
                    q.del_lrem(ii)
                except Exception as e:
                    print(e)
                    logge.error("nginx log 入库失败")

                continue
            break




            # ip = get_ip(nginx_log_msg["true_ip"])
            # ip_obj = IpInfo.objects.values("id", "ip").filter(ip=ip["ip"]).first()
            # if not ip_obj:
            #     try:
            #         o = IpInfo(**ip)
            #         logge.info("ip 入库成功")
            #         o.save()
            #     except Exception as e:
            #         print(e)
            #         q.put(result)
            #         logge.error("ip 入库失败")
            #         continue
            # try:
            #     log_ip = IpInfo.objects.values("id").filter(ip=nginx_log_msg["true_ip"]).first()
            #     nginx_log_msg.pop("true_ip")
            #     nginx_log_msg["true_ip_id"] = log_ip["id"]
            #     nginx_log_msg["projece_name"] = projece_name
            #     format1 = '%Y-%m-%dT%H:%M:%S+08:00'
            #     format2 = '%Y-%m-%d %H:%M:%S'
            #     t1 = nginx_log_msg["log_time"]
            #     t = time.strptime(t1, format1)
            #     t2 = time.strftime(format2, t)
            #     nginx_log_msg["log_time"] = t2
            #     nginx_list.append(NginxLog(**nginx_log_msg))
            #     count += 1
            #     continue
            # except Exception as e:
            #     print(e)
            #     q.put(result)
            #     logge.error("nginx log 入库失败")
            # continue



def get_inip_db(key,**redis_kwargs):
    logge = MyLogger()
    q = RedisQueue(key, **redis_kwargs)
    ipinfo_list = []
    ip_list = []
    start = -10000
    end = 0
    ip_len = q.qsize()

    while 1:
        if start > ip_len:
            logge.info("ip入库完成")
            break
        start += 10000
        end += 10000
        all_log = q.get_lrange(start,end)
        print(start,end)
        if len(ipinfo_list) != 0:
            IpInfo.objects.bulk_create(ipinfo_list)
            logge.info("ip 入库成功")
            ipinfo_list = []
        for i in all_log:

            # all_log[all_log.index(i)] = i.decode()
            nginx_log_dict = json.loads(i.decode())
            nginx_log_msg = json.loads(nginx_log_dict["message"])
            if nginx_log_msg["true_ip"] == "-":
                continue
            ip = get_ip(nginx_log_msg["true_ip"])

            ip_obj = IpInfo.objects.values("id", "ip").filter(ip=ip["ip"]).first()
            if not ip_obj:
                try:
                    o = IpInfo(**ip)
                    if o.ip in ip_list:
                        continue
                    ip_list.append(o.ip)
                    ipinfo_list.append(o)
                    print(ipinfo_list)
                except Exception as e:
                    print(e)
                continue
            break







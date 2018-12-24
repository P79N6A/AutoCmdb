from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from log_analyse import  models
from django.db.models import Count,Q,Sum
from log_analyse.models import NginxLog
from django.core.paginator import Paginator

class getNginxLogViews(View):
    dic_news = {
        "state": 0,
        "code": 0
        , "msg": ""
        , "count": 3000000
        , "data": []}
    def get(self, request, *args, **kwargs):

        return render(request, "log/ngx-log/index.html", locals())

    def post(self, request, *args, **kwargs):
        format2 = '%Y-%m-%dT%H:%M:%S'
        pageStart = request.POST.get("pageStart")
        pageSize = request.POST.get("pageSize")
        # print(request.POST.__dict__)

        # print(z)
        all_log = list(models.NginxLog.objects.values("projece_name","user_ip","log_time","user_req","http_code",
                                        "user_ua","true_ip__Country","true_ip__Subdivisions","true_ip__City",).order_by('log_time').all())
        # print(all_log)
        self.dic_news["count"] =len(all_log)
        self.dic_news["data"] = all_log
        paginator = Paginator(self.dic_news["data"], pageSize)
        self.dic_news["data"] = paginator.page(pageStart).object_list
        return JsonResponse( self.dic_news)

class getSearchLogViews(View):
    dic_news = {
        "state": 0,
        "code": 0
        , "msg": ""
        , "count": 3000000
        , "data": []}

    def post(self,request, *args, **kwargs):
        """
        项目。日志时间段。客户端真实IP。国家。省。市。
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pageStart = request.POST.get("pageStart")
        pageSize = request.POST.get("pageSize")
        projece_name = request.POST.get("projece_name")
        user_ip = request.POST.get("user_ip")
        date_time = request.POST.get("date_time")
        req_interface = request.POST.get("req_interface")
        country = request.POST.get("country")
        obj = NginxLog.objects.values("projece_name","user_ip","log_time","user_req","http_code",
                                        "user_ua","true_ip__Country","true_ip__Subdivisions","true_ip__City")
        if user_ip:
            obj = obj.filter(Q(user_ip=user_ip))
            print(1)
        if date_time:
            date_list = date_time.split(" - ")
            start_date = date_list[0]
            end_date = date_list[1]
            obj = obj.filter(Q(log_time__range=[start_date,end_date]))
            print(2)
        if req_interface:
            obj = obj.filter(Q(user_req__icontains=req_interface))
            print(3)
        if country:
            obj = obj.filter(Q(true_ip__Country__icontains=country) | Q(true_ip__City__icontains=country) |
                             Q(true_ip__Subdivisions__icontains=country))
            print(obj)
            print(4)
        all_log = list(obj.all())
        self.dic_news["count"] = len(all_log)
        self.dic_news["data"] = all_log
        print(pageStart)
        paginator = Paginator(self.dic_news["data"], pageSize)
        self.dic_news["data"] = paginator.page(pageStart).object_list

        return JsonResponse(self.dic_news)


class getlogInfoViews(View):
    dic_news = {
        "state": 0,
        "code": 0
        , "msg": ""
        , "count": 3000000
        , "data": []}
    def get(self, request, *args, **kwargs):
        return render(request, "log/ngx-log/ec-info.html", locals())


    def post(self, request, *args, **kwargs):
        """
        区域    访问量   访问占比

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        date_time = request.POST.get("date_time")
        projece_name = request.POST.get("projece_name")
        pageStart = request.POST.get("pageStart")
        pageSize = request.POST.get("pageSize")
        country = request.POST.get("country")
        obj = NginxLog.objects.values("projece_name","true_ip__Country", "true_ip__Subdivisions")

        z = NginxLog.objects
        if projece_name:
            z = z.filter(Q(projece_name=projece_name))
            obj = obj.filter(Q(projece_name=projece_name))
        if country:
            z = z.filter(Q(true_ip__Country__icontains=country) | Q(true_ip__City__icontains=country) |
                         Q(true_ip__Subdivisions__icontains=country))
            obj = obj.filter(Q(true_ip__Country__icontains=country) | Q(true_ip__City__icontains=country) |
                             Q(true_ip__Subdivisions__icontains=country))
        if date_time:
            date_list = date_time.split(" - ")
            start_date = date_list[0]
            end_date = date_list[1]
            z = z.filter(Q(log_time__range=[start_date, end_date]))
            obj = obj.filter(Q(log_time__range=[start_date, end_date]))
        z = z.values("id").all().count()
        all_log = list(
            obj.annotate(
                page_c=Count("true_ip")).order_by("-page_c")
        )  # 访问量



        for i in all_log:
            if not i["true_ip__Subdivisions"]:
                i["true_ip__Subdivisions"] = "未知"
            i["percent"] = '%.5f%%' % (i["page_c"] / z * 100)
        self.dic_news["count"] = len(all_log)
        self.dic_news["data"] = all_log
        print(pageStart)
        paginator = Paginator(self.dic_news["data"], pageSize)
        self.dic_news["data"] = paginator.page(pageStart).object_list
        return JsonResponse(self.dic_news)


class getlogIpViews(View):
    dic_news = {
        "state": 0,
        "code": 0
        , "msg": ""
        , "count": 3000000
        , "data": []}

    def get(self, request, *args, **kwargs):

        return render(request, "log/ngx-log/ec-ip.html", locals())

    def post(self, request, *args, **kwargs):
        """
        ip    次数
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        date_time = request.POST.get("date_time")
        pageStart = request.POST.get("pageStart")
        pageSize = request.POST.get("pageSize")
        projece_name = request.POST.get("projece_name")
        country = request.POST.get("country")
        user_ip = request.POST.get("user_ip")
        obj = NginxLog.objects.values("projece_name", "true_ip__ip", "true_ip__Country", "true_ip__Subdivisions",
                                    "true_ip__City")

        z = NginxLog.objects
        if projece_name:
            z = z.filter(Q(projece_name=projece_name))
            obj = obj.filter(Q(projece_name=projece_name))
        if user_ip:
            z = z.filter(Q(user_ip=user_ip))
            obj = obj.filter(Q(user_ip=user_ip))
        if country:
            z = z.filter(Q(true_ip__Country__icontains=country) | Q(true_ip__City__icontains=country) |
                             Q(true_ip__Subdivisions__icontains=country))
            obj = obj.filter(Q(true_ip__Country__icontains=country) | Q(true_ip__City__icontains=country) |
                             Q(true_ip__Subdivisions__icontains=country))
        if date_time:
            date_list = date_time.split(" - ")
            start_date = date_list[0]
            end_date = date_list[1]
            z = z.filter(Q(log_time__range=[start_date,end_date]))
            obj = obj.filter(Q(log_time__range=[start_date, end_date]))
        z = z.values("id").all().count()
        all_log = list(
            obj.annotate(
                page_c=Count("true_ip")).order_by("-page_c")
        )

        k = 0
        for i in all_log:
            k += i["page_c"]
            if not i["true_ip__Subdivisions"]:
                i["true_ip__Subdivisions"] = "未知"
            i["percent"] = '%.5f%%' % (i["page_c"] / z * 100)
        print(k)
        self.dic_news["count"] = len(all_log)
        self.dic_news["data"] = all_log
        print(pageStart)
        paginator = Paginator(self.dic_news["data"], pageSize)
        self.dic_news["data"] = paginator.page(pageStart).object_list
        return JsonResponse(self.dic_news)



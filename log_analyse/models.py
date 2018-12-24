from django.db import models

# Create your models here.

class IpInfo(models.Model):
    ip = models.GenericIPAddressField(verbose_name="IP地址",unique=True)
    Country = models.CharField(verbose_name="国家",max_length=32)
    # country_code = models.CharField(verbose_name="国家缩写",max_length=32)
    Subdivisions = models.CharField(verbose_name="省",max_length=32,null=True,blank=True)
    City = models.CharField(verbose_name="市",max_length=32,null=True,blank=True)
    # city_code = models.CharField(verbose_name="城市代码",max_length=32,null=True,blank=True)
    # city_short_code = models.CharField(verbose_name="城市代码缩写",max_length=32,null=True,blank=True)
    # Area = models.CharField(verbose_name="区域",max_length=32,null=True,blank=True)
    # area_code = models.CharField(verbose_name="区号",max_length=32,null=True,blank=True)
    # Isp = models.CharField(verbose_name="运营商",max_length=32,null=True,blank=True)
    Latitude = models.CharField(verbose_name="纬度",max_length=32,null=True,blank=True)
    Longitude = models.CharField(verbose_name="经度",max_length=32,null=True,blank=True)
    # big_area = models.CharField(verbose_name="大区",max_length=32,null=True,blank=True)


class NginxLog(models.Model):
    projece_name = models.CharField(max_length=64,verbose_name="项目名")
    user_ip = models.GenericIPAddressField(verbose_name="客户端真实IP",null=True,blank=True)
    lan_ip = models.GenericIPAddressField(verbose_name="客户端代理ip")
    log_time = models.DateTimeField(verbose_name="日志时间",max_length=64)
    user_req = models.CharField(verbose_name="用户请求",max_length=1024)
    http_code = models.CharField(verbose_name="状态返回码",max_length=64)
    body_bytes_sents = models.CharField(verbose_name="客户端返回字节数",max_length=64)
    req_time = models.CharField(verbose_name="请求花费时间",max_length=64)
    user_ua = models.CharField(verbose_name="用户代理",max_length=512)
    true_ip = models.ForeignKey(to=IpInfo,verbose_name="真实IP地址",on_delete=models.CASCADE)

    # class Meta:
    #     unique_together = ('user_ip', 'log_time',)


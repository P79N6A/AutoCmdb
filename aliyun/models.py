from django.db import models

# Create your models here.


class Region(models.Model):
    State = (
        (0, u'中国大陆'),
        (1, u'其他国家和地区'),
    )
    RegionId = models.CharField(max_length=64,verbose_name="Region ID", unique=True)
    RegionName = models.CharField(max_length=32,verbose_name="地域名称",)
    RegionCity = models.CharField(max_length=32,verbose_name="所在城市")
    RegionNumber = models.IntegerField(verbose_name="可用区数量", null=True)
    RegionState = models.IntegerField(choices=State,verbose_name="国属",null=True)

    class Meta:
        verbose_name_plural = "阿里地域表"

    def __str__(self):
        return "%s" % (self.RegionId)


class AliEcs(models.Model):
    InnerIpAddress_IpAddress = models.CharField(max_length=64,verbose_name="内网地址",null=True,blank=True)
    ImageId = models.CharField(max_length=64,verbose_name="镜像ID",null=True,blank=True)
    InstanceTypeFamily = models.CharField(max_length=64,verbose_name="实例规格族",null=True,blank=True)
    VlanId = models.CharField(max_length=64,verbose_name="VlanId",null=True,blank=True)
    NetworkInterfaces_NetworkInterface_MacAddress = models.CharField(max_length=128,verbose_name="Mac地址",null=True,blank=True)
    NetworkInterfaces_NetworkInterface_PrimaryIpAddress = models.CharField(max_length=128,verbose_name="主私有IP地址",null=True,blank=True)
    NetworkInterfaces_NetworkInterface_NetworkInterfaceId = models.CharField(max_length=128,verbose_name="弹性网卡ID",null=True,blank=True)
    InstanceId = models.CharField(max_length=64,unique=True,verbose_name="实例ID")
    EipAddress_IpAddress = models.CharField(max_length=64,verbose_name="ip地址",null=True,blank=True)
    EipAddress_AllocationId = models.CharField(max_length=64,verbose_name="ip地址分配ID",null=True,blank=True)
    EipAddress_InternetChargeType = models.CharField(max_length=64,null=True,blank=True)
    InternetMaxBandwidthIn = models.IntegerField(verbose_name="网络最大入口带宽",null=True,blank=True)
    CreditSpecification = models.CharField(max_length=64,null=True,blank=True)
    ZoneId = models.CharField(max_length=64,verbose_name="可用区ID",null=True,blank=True)
    InternetChargeType = models.CharField(max_length=64,verbose_name="带宽计费方式",null=True,blank=True)
    SpotStrategy = models.CharField(max_length=128,null=True,blank=True)
    StoppedMode = models.CharField(max_length=64,verbose_name="停止模式",null=True,blank=True)
    SerialNumber = models.CharField(max_length=64,verbose_name="序列号",null=True,blank=True)
    IoOptimized = models.BooleanField(max_length=32,blank=True)
    Memory = models.IntegerField(verbose_name="内存",null=True,blank=True)
    Cpu = models.IntegerField(verbose_name="CPU",null=True,blank=True)
    VpcAttributes_NatIpAddress = models.CharField(max_length=128,blank=True)
    VpcAttributes_PrivateIpAddress_IpAddress = models.CharField(max_length=128,verbose_name="vpcIP",null=True,blank=True)
    VpcAttributes_VSwitchId = models.CharField(max_length=128,verbose_name="vpc交换机ID",null=True,blank=True)
    VpcAttributes_VpcId = models.CharField(max_length=128,verbose_name="vpcID",null=True,blank=True)
    InternetMaxBandwidthOut = models.IntegerField(verbose_name="网络最大出口带宽",null=True,blank=True)
    DeviceAvailable = models.BooleanField(max_length=64,verbose_name="设备可用性",blank=True)
    SecurityGroupIds_SecurityGroupId = models.CharField(max_length=64,verbose_name="安全组",null=True,blank=True)
    SaleCycle = models.CharField(max_length=64,null=True,blank=True)
    SpotPriceLimit = models.FloatField(max_length=32,null=True,blank=True)
    AutoReleaseTime = models.CharField(max_length=64,null=True,blank=True)
    StartTime = models.CharField(max_length=64,verbose_name="启动时间",null=True,blank=True)
    InstanceName = models.CharField(max_length=64,verbose_name="实例名",null=True,blank=True)
    Description = models.CharField(max_length=128,verbose_name="描述",null=True,blank=True)
    ResourceGroupId = models.CharField(max_length=64,null=True,blank=True)
    OSType = models.CharField(max_length=64,verbose_name="系统类型",null=True,blank=True)
    OSName = models.CharField(max_length=64,verbose_name="系统名",null=True,blank=True)
    InstanceNetworkType = models.CharField(max_length=64,verbose_name="动态网络类型",null=True,blank=True)
    PublicIpAddress_IpAddress = models.CharField(max_length=64,verbose_name="公共IP地址",null=True,blank=True)
    HostName = models.CharField(max_length=64,verbose_name="主机名",null=True,blank=True)
    InstanceType = models.CharField(max_length=64,verbose_name="实例类型",null=True,blank=True)
    CreationTime = models.CharField(max_length=64,verbose_name="创建时间",null=True,blank=True)
    Status = models.CharField(max_length=32,verbose_name="状态",null=True,blank=True)
    ClusterId = models.CharField(max_length=32,verbose_name="集群",null=True,blank=True)
    Recyclable = models.BooleanField(max_length=32,verbose_name="是否可回收",blank=True)
    # RegionId = models.CharField(max_length=32,verbose_name="区域",null=True,blank=True)
    RegionId = models.ForeignKey("Region",on_delete=models.CASCADE)
    GPUSpec = models.CharField(max_length=32,verbose_name="GPU规格",null=True,blank=True)
    DedicatedHostAttribute_DedicatedHostId = models.CharField(max_length=64,null=True,blank=True)
    DedicatedHostAttribute_DedicatedHostName = models.CharField(max_length=64,null=True,blank=True)
    OperationLocks_LockReason = models.CharField(max_length=64,null=True,blank=True)
    GPUAmount = models.IntegerField(verbose_name="GPU数量",null=True,blank=True)
    InstanceChargeType = models.CharField(max_length=32,verbose_name="实例计费类型",null=True,blank=True)
    ExpiredTime = models.CharField(max_length=64,verbose_name="到期时间",null=True,blank=True)
    DeploymentSetId = models.CharField(max_length=32,null=True,blank=True)
    account = models.ForeignKey("AliAccount",on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "阿里ECS表"

    def __str__(self):
        return "%s" % (self.HostName)


class AliAccount(models.Model):
    accountName = models.CharField(max_length=128,verbose_name="账号名")
    accessKey = models.CharField(max_length=128,verbose_name="accessKey")
    accessSecret = models.CharField(max_length=128,verbose_name="accessSecret")
    region = models.ManyToManyField("Region",verbose_name="可用区")


    class Meta:
        verbose_name_plural = "阿里账号表"

    def __str__(self):
        return "%s"%(self.accountName)


# class AliDomain(models.Model):
#     account = models.ForeignKey("AliAccount")
#     RegistrationDateLong = models.BigIntegerField(max_length=64,verbose_name="")
#     InstanceId = models.CharField(max_length=64,verbose_name="")
#     DomainStatus = models.CharField(max_length=32,verbose_name="")
#     ExpirationDateStatus = models.CharField(max_length=32,verbose_name="")
#     DomainAuditStatus = models.CharField(max_length=32,verbose_name="")
#     ExpirationDateLong = models.IntegerField(max_length=32,verbose_name="")
#     Premium = models.BooleanField(verbose_name="")
#     ProductId = models.CharField(max_length=32,verbose_name="")
#     ExpirationDate = models.DateField(verbose_name="")
#     RegistrantType = models.CharField(max_length=32,verbose_name="")
#     RegistrationDate = models.DateField(verbose_name="")
#     DomainName = models.CharField(max_length=32,verbose_name="域名")
#     DomainType = models.CharField(max_length=32,verbose_name="域名类型")
#     ExpirationCurrDateDiff = models.IntegerField(max_length=32,verbose_name="")

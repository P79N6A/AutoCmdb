# Generated by Django 2.1.3 on 2018-12-10 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AliAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accountName', models.CharField(max_length=128, verbose_name='账号名')),
                ('accessKey', models.CharField(max_length=128, verbose_name='accessKey')),
                ('accessSecret', models.CharField(max_length=128, verbose_name='accessSecret')),
            ],
            options={
                'verbose_name_plural': '阿里账号表',
            },
        ),
        migrations.CreateModel(
            name='AliEcs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('InnerIpAddress_IpAddress', models.CharField(blank=True, max_length=64, null=True, verbose_name='内网地址')),
                ('ImageId', models.CharField(blank=True, max_length=64, null=True, verbose_name='镜像ID')),
                ('InstanceTypeFamily', models.CharField(blank=True, max_length=64, null=True, verbose_name='实例规格族')),
                ('VlanId', models.CharField(blank=True, max_length=64, null=True, verbose_name='VlanId')),
                ('NetworkInterfaces_NetworkInterface_MacAddress', models.CharField(blank=True, max_length=128, null=True, verbose_name='Mac地址')),
                ('NetworkInterfaces_NetworkInterface_PrimaryIpAddress', models.CharField(blank=True, max_length=128, null=True, verbose_name='主私有IP地址')),
                ('NetworkInterfaces_NetworkInterface_NetworkInterfaceId', models.CharField(blank=True, max_length=128, null=True, verbose_name='弹性网卡ID')),
                ('InstanceId', models.CharField(max_length=64, unique=True, verbose_name='实例ID')),
                ('EipAddress_IpAddress', models.CharField(blank=True, max_length=64, null=True, verbose_name='ip地址')),
                ('EipAddress_AllocationId', models.CharField(blank=True, max_length=64, null=True, verbose_name='ip地址分配ID')),
                ('EipAddress_InternetChargeType', models.CharField(blank=True, max_length=64, null=True)),
                ('InternetMaxBandwidthIn', models.IntegerField(blank=True, null=True, verbose_name='网络最大入口带宽')),
                ('CreditSpecification', models.CharField(blank=True, max_length=64, null=True)),
                ('ZoneId', models.CharField(blank=True, max_length=64, null=True, verbose_name='可用区ID')),
                ('InternetChargeType', models.CharField(blank=True, max_length=64, null=True, verbose_name='带宽计费方式')),
                ('SpotStrategy', models.CharField(blank=True, max_length=128, null=True)),
                ('StoppedMode', models.CharField(blank=True, max_length=64, null=True, verbose_name='停止模式')),
                ('SerialNumber', models.CharField(blank=True, max_length=64, null=True, verbose_name='序列号')),
                ('IoOptimized', models.BooleanField(blank=True, max_length=32)),
                ('Memory', models.IntegerField(blank=True, null=True, verbose_name='内存')),
                ('Cpu', models.IntegerField(blank=True, null=True, verbose_name='CPU')),
                ('VpcAttributes_NatIpAddress', models.CharField(blank=True, max_length=128)),
                ('VpcAttributes_PrivateIpAddress_IpAddress', models.CharField(blank=True, max_length=128, null=True, verbose_name='vpcIP')),
                ('VpcAttributes_VSwitchId', models.CharField(blank=True, max_length=128, null=True, verbose_name='vpc交换机ID')),
                ('VpcAttributes_VpcId', models.CharField(blank=True, max_length=128, null=True, verbose_name='vpcID')),
                ('InternetMaxBandwidthOut', models.IntegerField(blank=True, null=True, verbose_name='网络最大出口带宽')),
                ('DeviceAvailable', models.BooleanField(blank=True, max_length=64, verbose_name='设备可用性')),
                ('SecurityGroupIds_SecurityGroupId', models.CharField(blank=True, max_length=64, null=True, verbose_name='安全组')),
                ('SaleCycle', models.CharField(blank=True, max_length=64, null=True)),
                ('SpotPriceLimit', models.FloatField(blank=True, max_length=32, null=True)),
                ('AutoReleaseTime', models.CharField(blank=True, max_length=64, null=True)),
                ('StartTime', models.CharField(blank=True, max_length=64, null=True, verbose_name='启动时间')),
                ('InstanceName', models.CharField(blank=True, max_length=64, null=True, verbose_name='实例名')),
                ('Description', models.CharField(blank=True, max_length=128, null=True, verbose_name='描述')),
                ('ResourceGroupId', models.CharField(blank=True, max_length=64, null=True)),
                ('OSType', models.CharField(blank=True, max_length=64, null=True, verbose_name='系统类型')),
                ('OSName', models.CharField(blank=True, max_length=64, null=True, verbose_name='系统名')),
                ('InstanceNetworkType', models.CharField(blank=True, max_length=64, null=True, verbose_name='动态网络类型')),
                ('PublicIpAddress_IpAddress', models.CharField(blank=True, max_length=64, null=True, verbose_name='公共IP地址')),
                ('HostName', models.CharField(blank=True, max_length=64, null=True, verbose_name='主机名')),
                ('InstanceType', models.CharField(blank=True, max_length=64, null=True, verbose_name='实例类型')),
                ('CreationTime', models.CharField(blank=True, max_length=64, null=True, verbose_name='创建时间')),
                ('Status', models.CharField(blank=True, max_length=32, null=True, verbose_name='状态')),
                ('ClusterId', models.CharField(blank=True, max_length=32, null=True, verbose_name='集群')),
                ('Recyclable', models.BooleanField(blank=True, max_length=32, verbose_name='是否可回收')),
                ('GPUSpec', models.CharField(blank=True, max_length=32, null=True, verbose_name='GPU规格')),
                ('DedicatedHostAttribute_DedicatedHostId', models.CharField(blank=True, max_length=64, null=True)),
                ('DedicatedHostAttribute_DedicatedHostName', models.CharField(blank=True, max_length=64, null=True)),
                ('OperationLocks_LockReason', models.CharField(blank=True, max_length=64, null=True)),
                ('GPUAmount', models.IntegerField(blank=True, null=True, verbose_name='GPU数量')),
                ('InstanceChargeType', models.CharField(blank=True, max_length=32, null=True, verbose_name='实例计费类型')),
                ('ExpiredTime', models.CharField(blank=True, max_length=64, null=True, verbose_name='到期时间')),
                ('DeploymentSetId', models.CharField(blank=True, max_length=32, null=True)),
            ],
            options={
                'verbose_name_plural': '阿里ECS表',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RegionId', models.CharField(max_length=64, unique=True, verbose_name='Region ID')),
                ('RegionName', models.CharField(max_length=32, verbose_name='地域名称')),
                ('RegionCity', models.CharField(max_length=32, verbose_name='所在城市')),
                ('RegionNumber', models.IntegerField(null=True, verbose_name='可用区数量')),
                ('RegionState', models.IntegerField(choices=[(0, '中国大陆'), (1, '其他国家和地区')], null=True, verbose_name='国属')),
            ],
            options={
                'verbose_name_plural': '阿里地域表',
            },
        ),
        migrations.AddField(
            model_name='aliecs',
            name='RegionId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aliyun.Region'),
        ),
        migrations.AddField(
            model_name='aliecs',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aliyun.AliAccount'),
        ),
        migrations.AddField(
            model_name='aliaccount',
            name='region',
            field=models.ManyToManyField(to='aliyun.Region', verbose_name='可用区'),
        ),
    ]

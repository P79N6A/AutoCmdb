# Generated by Django 2.1.3 on 2018-12-17 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IpInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(unique=True, verbose_name='IP地址')),
                ('Country', models.CharField(max_length=32, verbose_name='国家')),
                ('Subdivisions', models.CharField(blank=True, max_length=32, null=True, verbose_name='省')),
                ('City', models.CharField(blank=True, max_length=32, null=True, verbose_name='市')),
                ('Latitude', models.CharField(blank=True, max_length=32, null=True, verbose_name='纬度')),
                ('Longitude', models.CharField(blank=True, max_length=32, null=True, verbose_name='经度')),
            ],
        ),
        migrations.CreateModel(
            name='NginxLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projece_name', models.CharField(max_length=64, verbose_name='项目名')),
                ('user_ip', models.GenericIPAddressField(verbose_name='客户端真实IP')),
                ('lan_ip', models.GenericIPAddressField(verbose_name='客户端代理ip')),
                ('log_time', models.CharField(max_length=64, verbose_name='日志时间')),
                ('user_req', models.CharField(max_length=1024, verbose_name='用户请求')),
                ('http_code', models.CharField(max_length=64, verbose_name='状态返回码')),
                ('body_bytes_sents', models.CharField(max_length=64, verbose_name='客户端返回字节数')),
                ('req_time', models.CharField(max_length=64, verbose_name='请求花费时间')),
                ('user_ua', models.CharField(max_length=512, verbose_name='用户代理')),
                ('true_ip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='log_analyse.IpInfo', verbose_name='真实IP地址')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='nginxlog',
            unique_together={('user_ip', 'log_time')},
        ),
    ]

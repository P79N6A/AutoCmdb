# Generated by Django 2.1.3 on 2018-12-05 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_login',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='login_sta',
            field=models.CharField(default=0, max_length=2, verbose_name='登录是否锁定'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='login_suo',
            field=models.DateTimeField(default=0, verbose_name='登录锁定时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='pass_errn',
            field=models.IntegerField(default=0, verbose_name='用户密码输入次数'),
        ),
    ]

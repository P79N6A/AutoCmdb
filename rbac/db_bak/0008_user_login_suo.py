# Generated by Django 2.1.3 on 2018-12-05 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0007_user_is_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='login_suo',
            field=models.DateTimeField(default=0, verbose_name='登录锁定时间'),
            preserve_default=False,
        ),
    ]
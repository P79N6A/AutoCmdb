# Generated by Django 2.1.3 on 2018-12-05 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0002_auto_20181205_1239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_login',
        ),
        migrations.RemoveField(
            model_name='user',
            name='login_suo',
        ),
        migrations.RemoveField(
            model_name='user',
            name='pass_errnum',
        ),
    ]

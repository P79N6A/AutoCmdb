# Generated by Django 2.1.3 on 2018-12-18 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_analyse', '0002_auto_20181218_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nginxlog',
            name='user_ip',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='客户端真实IP'),
        ),
    ]
# Generated by Django 2.1.3 on 2018-12-18 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_analyse', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nginxlog',
            name='log_time',
            field=models.DateTimeField(max_length=64, verbose_name='日志时间'),
        ),
    ]

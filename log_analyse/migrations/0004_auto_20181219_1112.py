# Generated by Django 2.1.4 on 2018-12-19 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log_analyse', '0003_auto_20181218_1051'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='nginxlog',
            unique_together=set(),
        ),
    ]
# Generated by Django 2.1.3 on 2018-12-05 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0002_auto_20181205_1332'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='is_login',
            new_name='isNot_login',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='login_suo',
            new_name='login_lock_date',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='login_sta',
            new_name='login_state',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='pass_errn',
            new_name='pass_err_count',
        ),
    ]

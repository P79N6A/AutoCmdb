# Generated by Django 2.1.3 on 2018-12-05 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0006_remove_user_is_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_login',
            field=models.BooleanField(default=False),
        ),
    ]

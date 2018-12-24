from django.contrib import admin
from aliyun import models

# Register your models here.

admin.site.register(models.AliEcs)
admin.site.register(models.Region)
admin.site.register(models.AliAccount)
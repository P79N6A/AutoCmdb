from django.contrib import admin
from log_analyse import models

# Register your models here.
admin.site.register(models.IpInfo)
admin.site.register(models.NginxLog)
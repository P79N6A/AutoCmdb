from django.conf.urls import url,include
from django.contrib import admin
from log_analyse.views import getNginxLogViews,getSearchLogViews,getlogInfoViews,getlogIpViews


urlpatterns = [
    # url(r'^admin/', admin.site.urls)
    url(r'^$',getNginxLogViews.as_view(),name="getNginxLog"),
    url(r'^get-search-log$',getSearchLogViews.as_view(),name="getSearchLogViews"),
    url(r'^logInfo',getlogInfoViews.as_view(),name="getlogInfo"),
    url(r'^ipInfo',getlogIpViews.as_view(),name="getlogIp"),

]

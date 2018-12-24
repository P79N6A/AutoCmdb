from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from web.views import account
from web.views import home
from web.views import asset
from web.views import user


urlpatterns = [
    url(r'^pc-geetest/register/$', account.pcgetcaptcha, name='pcgetcaptcha'),
    url(r'^basic.html$', account.BaseView.as_view()),
    url(r'^login/$', account.acc_login,name="login"),
    url(r'^logout/$', account.acc_logout,name="logout"),
    url(r'^index.html$', home.IndexView.as_view(),name="index"),
    url(r'^cmdb.html$', home.CmdbView.as_view()),
    url(r'^asset.html$', asset.AssetListView.as_view()),
    url(r'^assets.html$', asset.AssetJsonView.as_view()),
    url(r'^asset-(?P<device_type_id>\d+)-(?P<asset_nid>\d+).html$', asset.AssetDetailView.as_view()),
    url(r'^add-asset.html$', asset.AddAssetView.as_view()),

    url(r'^web/static/demo.json',account.TestView.as_view()),
    url(r'^users.html$', user.UserListView.as_view()),
    url(r'^user.html$', user.UserJsonView.as_view()),

    url(r'^chart-(?P<chart_type>\w+).html$', home.ChartView.as_view()),

    # url(r'^userinfo/add/$', views.userinfo_add),
    # url(r'^userinfo/del/(\d+)/$', views.userinfo_del),
    # url(r'^userinfo/edit/(\d+)/$', views.userinfo_edit),
    # url(r'^order/$', views.order),
    # url(r'^order/add/$', views.order_add),
    # url(r'^order/del/(\d+)/$', views.order_del),
    # url(r'^order/edit/(\d+)/$', views.order_edit),


]

from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from api import views
from config.views import rule

urlpatterns = [
    url(r'^role$', rule.ruleView.as_view(), name="role"),
]

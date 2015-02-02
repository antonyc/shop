# coding: utf-8

from django.conf.urls import patterns, include, url

from .views import (
    PageView,
)

urlpatterns = patterns(
    '',
    url(r'(?P<pk>\d+)/$', PageView.as_view(), name='view'),
)

# coding: utf-8

from django.conf.urls import patterns, include, url

from .views import (
    CreatePage, ListPages, UpdatePage, DeletePage
)

urlpatterns = patterns(
    '',
    url(r'create/$', CreatePage.as_view(), name='page_create'),
    url(r'(?P<pk>\d+)/$', UpdatePage.as_view(), name='page_update'),
    url(r'(?P<pk>\d+)/delete/$', DeletePage.as_view(), name='page_delete'),
    url(r'$', ListPages.as_view(), name='page_list'),
)

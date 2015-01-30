from django.conf.urls.defaults import *
from administration.users.views import ListUsers, ShowUser, EditUser

urlpatterns = patterns('',
    url(r'(?P<id>\d+)/edit/$', EditUser.as_view(), name='edit_user'),
    url(r'add/$', EditUser.as_view(), name='add_user'),
    url(r'(?P<id>\d+)/$', ShowUser.as_view(), name='show_user'),
    url(r'$', ListUsers.as_view(), name='list_users'),
)
from django.conf.urls.defaults import *
from users.views import LoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('',
    url(r'login/$', LoginView.as_view(), name='user_login'),
    url(r'final_step/$', 'users.views.complete_registration', name='loginza_login'),
    url(r'logout/$', LogoutView.as_view(), name='user_logout'),
)
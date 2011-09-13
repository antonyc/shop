from django.conf.urls.defaults import *

from pages.views import ShowPageView

urlpatterns = patterns(
    '',
    url(r'(?P<url>[\w\-]+)/$', ShowPageView.as_view(), name='show_page'),
)

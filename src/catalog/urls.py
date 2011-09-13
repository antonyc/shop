from django.conf.urls.defaults import *
from catalog.views import ShowItemView

urlpatterns = patterns('',
    url(r'item/(?P<url>[\w\-]+)/$', ShowItemView.as_view(), name='show_item'),
    # Examples:
    # url(r'^$', 'shop.views.home', name='home'),
    # url(r'^shop/', include('shop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)


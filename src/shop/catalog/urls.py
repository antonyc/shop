from django.conf.urls.defaults import *
from catalog.views import ShowItemView, ShowCategoryView

urlpatterns = patterns('',
    url(r'item/(?P<url>[\w\-]+)/$', ShowItemView.as_view(), name='show_item'),
    url(r'category/(?P<url>[\w\-/]+)/$', ShowCategoryView.as_view(), name='show_category'),
    url(r'$', ShowCategoryView.as_view(), name='show_category'),
    # Examples:
    # url(r'^$', 'shop.views.home', name='home'),
    # url(r'^shop/', include('shop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)


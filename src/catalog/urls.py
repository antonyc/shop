from django.conf.urls.defaults import patterns, include, url
from urlparse import urlparse
from catalog.models import Item, Category
from catalog.views import show_item
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

def dispatcher(request):
    raise Exception(request)
    purl = urlparse(request.META['PATH_INFO'])
    url = purl.strip('/').lower()
    try:
        item = Item.objects.get(url=url)
    except Item.DoesNotExist:
        pass
    else:
        return show_item(request)


urlpatterns = patterns('',
    url(r'.*$', dispatcher)
    # Examples:
    # url(r'^$', 'shop.views.home', name='home'),
    # url(r'^shop/', include('shop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)


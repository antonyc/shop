from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
from catalog.views import ShowCategoryView

#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # Uncomment the next line to enable the admin:
    url(r'^administration/', include('administration.urls')),
#    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('users.urls')),
    url(r'^loginza/', include('loginza.urls')),
    url(r'^page/', include('pages.urls')),
    url(r'^catalog/', include('catalog.urls')),
    url(r'^orders/', include('orders.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^geocoding/', include('geocoding.urls')),
)


if settings.DEBUG:
#    from django.conf.urls.static import static
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }))
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
#    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += patterns('',
    url(r'^$', ShowCategoryView.as_view())
)

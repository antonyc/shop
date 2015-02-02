from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    # url(r'^$', 'lostpets.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/pages/', include('pages_admin.urls', namespace='admin')),
    url(r'^pages/', include('pages_public.urls', namespace='pages')),
)

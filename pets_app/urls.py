from django.conf.urls import patterns, include, url

from pets.views import ImageUploadView, PetsView, PetsListView

urlpatterns = patterns('',
    # url(r'^$', 'lostpets.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^api/v1/images/', ImageUploadView.as_view()),
    url(r'^api/v1/pets/(?P<id>[\da-zA-Z]+)/', PetsView.as_view(), name='pets_view'),
    url(r'^api/v1/pets/', PetsListView.as_view()),
)

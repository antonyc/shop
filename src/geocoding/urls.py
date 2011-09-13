from django.conf.urls.defaults import *
from geocoding.views import GeoSelectionHandleView

urlpatterns = patterns(
    '',
    url(r'resolve/(?P<fclass>country)/$', GeoSelectionHandleView.as_view(), name='resolve_geoname_country'),
    url(r'resolve/country/(?P<geonameid>\d+)/(?P<fclass>city)/$', GeoSelectionHandleView.as_view(), name='resolve_geoname_city'),
)
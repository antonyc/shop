# -*- coding:utf-8 -*-
from utils.base_view import BaseTemplateView
from django.http import Http404, HttpResponse
from django.db import models
from django.utils import simplejson
from urlparse import urlparse
from local_settings import HOST_NAME
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from geocoding.models import Geoalternate, Geomodel, GeoPlaceType

MAX_AUTOCOMPLETE_RESULTS = 10

def check_referer(orig_view_func):
    def view(request, *args, **kwargs):
        if 'HTTP_REFERER' not in request.META:
            return HttpResponse(status=403)
        preferer = urlparse(request.META['HTTP_REFERER'])
        if preferer.netloc != HOST_NAME:
            return HttpResponse(status=403)
        return orig_view_func(request, *args, **kwargs)
    return view

class GeoSelectionHandleView(BaseTemplateView):
    """
    Helps you get countries, cities for the client side
    """
    def resolve_country(self, subject, language, *args, **kwargs):
        variants = Geoalternate.objects.filter(variant__istartswith=subject).\
            filter(models.Q(isolanguage=language)|models.Q(isolanguage='')).\
            order_by('-preferred', 'short', 'variant',).\
            values('variant', 'isolanguage', 'geoname_id', 'preferred')[:100]
        hash = []
        results = []
        results_count = 0
        if variants.count() > 0:
            for alt in variants:
                if alt['geoname_id'] not in hash:
                    results_count += 1
                    if alt['isolanguage'] or alt['preferred']:
                        results.append({'name': alt['variant'],
                                        'geonameid': alt['geoname_id'],
                                        })
                    hash.append(alt['geoname_id'])
                if results_count == MAX_AUTOCOMPLETE_RESULTS:
                    break
        if len(results) == 0:
            results = Geomodel.objects.filter(name__istartswith=subject, typ=GeoPlaceType.country).\
                order_by('name').\
                values('name', 'geonameid')[:MAX_AUTOCOMPLETE_RESULTS]
            results = list(results)
        return HttpResponse(simplejson.dumps({'countries': results}),
                            mimetype='application/json')
    
    def resolve_city(self, subject, country_gid, language):
        try:
            country = Geomodel.objects.get(typ=GeoPlaceType.country, geonameid=country_gid)
        except Geomodel.DoesNotExist:
            return Http404()
        variants_qs = Geoalternate.objects.filter(variant__istartswith=subject).\
                        filter(geoname__typ=GeoPlaceType.city, geoname__country_code=country.country_code).\
                        filter(models.Q(isolanguage=language)|models.Q(isolanguage=''))
        variants = variants_qs.order_by('-preferred', 'short', 'variant',).\
            values('variant', 'isolanguage', 'geoname_id', 'preferred')
        results = []
        if variants_qs.count() > 0:
            hash = []
            for variant in variants:
                if variant['geoname_id'] not in hash or variant['preferred']:
                    hash.append(variant['geoname_id'])
                    results.append({'geonameid': variant['geoname_id'],
                                    'name': variant['variant'],})
                if len(results) == MAX_AUTOCOMPLETE_RESULTS:
                    break
        if len(results) == 0:
            results = Geomodel.objects.filter(name__istartswith=subject, typ=GeoPlaceType.city).\
                order_by('name').\
                values('name', 'geonameid')[:MAX_AUTOCOMPLETE_RESULTS]
            results = list(results)
        return HttpResponse(simplejson.dumps({'cities': results}),
                            mimetype='application/json')
    
            
    
    @method_decorator(check_referer)
    def get(self, request, fclass, *args, **kwargs):
        subject = self.request.GET.get('subject', '')
        if len(subject) < 1:
            return Http404()
        strategies = {'country': self.resolve_country,
                      'city': self.resolve_city}
        strategy = strategies.get(fclass)
        language = self.request.LANGUAGE_CODE[:2].lower()
        if 'country' == fclass:
            return self.resolve_country(subject, language)
        elif 'city' == fclass:
            return self.resolve_city(subject, kwargs.pop('geonameid'), language)
        return HttpResponse(status=403)
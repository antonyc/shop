# -*- coding: utf-8 -*-
from django.utils import simplejson
from django_dynamic_fixture import get
from django.test.testcases import TestCase
from django.core.urlresolvers import reverse
from urllib import urlencode
from django.conf import settings
from geocoding.models import Geomodel, Geoalternate, GeoPlaceType
from utils.base_testcase import BaseTestCase

class ShowPageTest(BaseTestCase):
    
    def setUp(self):
        super(ShowPageTest, self).setUp()
        self.setGeoNames()
        self.client.logout()
    
    def test_get_countries(self):
        base_url = reverse('resolve_geoname_country', kwargs={'fclass': 'country'})
        result = self.client.get(base_url, data={'subject': 'Irku'})
        self.failIfEqual(result.status_code, 200, "You should specify http referrer to do that")
        headers = {'HTTP_REFERER': 'http://%s/somepage/' % settings.HOST_NAME,
                   }
        result = self.client.get(base_url, data={'subject': 'Irku'}, **headers)
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")
        data = simplejson.loads(result.content)
        self.failUnless('countries' in data, "Must have country key in data")
        self.failUnlessEqual(len(data['countries']), 0, "Must be no such country")
        
        result = self.client.get(base_url, data={'subject': 'Russi'}, **headers)
        data = simplejson.loads(result.content)
        self.failUnlessEqual(len(data['countries']), 1, "Must be 1 country")
        keys_of_country = ('name', 'geonameid')
        for key in keys_of_country:
            self.failUnless(key in data['countries'][0], "Must have key (%s) in data" % key)

        result = self.client.get(base_url, data={'subject': 'Росси'}, **headers)
        data = simplejson.loads(result.content)
        self.failUnlessEqual(len(data['countries']), 0, "Must be no countries, cause default lang is EN")

        
        headers['HTTP_ACCEPT_LANGUAGE'] = 'ru-ru'
        result = self.client.get(base_url, data={'subject': 'Росси'}, **headers)
        data = simplejson.loads(result.content)
        self.failUnlessEqual(len(data['countries']), 1, "Must be 1 country")
        
    def test_get_cities(self):
        base_url = reverse('resolve_geoname_city', kwargs={'fclass': 'city', 'geonameid': self.russian_federation.geonameid})
        headers = {'HTTP_REFERER': 'http://%s/somepage/' % settings.HOST_NAME,
                   'HTTP_ACCEPT_LANGUAGE': 'ru-ru',
                   }
        result = self.client.get(base_url, data={'subject': u'Ирку'}, **headers)
        data = simplejson.loads(result.content)
        self.failUnless('cities' in data, "Must have cities in data")
        self.failUnlessEqual(len(data['cities']), 1, "Must have 1 city")
        keys_of_city = ['name', 'geonameid']
        for key in keys_of_city:
            self.failUnless(key in data['cities'][0], "Must have key (%s) in data" % key)
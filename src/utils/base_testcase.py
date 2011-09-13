# -*- coding:utf-8 -*-
import utils
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from pymongo import Connection
from geocoding.models import Geomodel, Geoalternate, GeoPlaceType
from django_dynamic_fixture import get
if not hasattr(settings, 'MONGO_DATABASES'):
    raise ImproperlyConfigured('You should configure mongo databases')

utils.mongo_connection = Connection(host=utils.mongo_settings['HOST'])

class BaseTestCase(TestCase):
    fixtures = ['categories.json']
    def setUpMongo(self):
        self.mongo_settings = settings.MONGO_DATABASES['default']
        db_name = 'test_'+self.mongo_settings['NAME']
        utils.mongo_db = getattr(utils.mongo_connection, 'test_' + utils.mongo_settings['NAME'])

    def setUp(self):
        self.setUpMongo()
        self.user = User.objects.create_superuser('chapson', 'mrdark@list.ru', '1')
        self.user1 = User.objects.create_superuser('zver', 'anton@list.ru', '1')
        self.client.login(username='zver', password='1')

    geonames_set = False
    def setGeoNames(self):
        if self.geonames_set:
            return
        self.geonames_set = True
        get(Geomodel, geonameid=2635167,
            name="United Kingdom of Great Britain and Northern Ireland",
            typ=GeoPlaceType.country,
            country_code="GB",
            parent=None)
        self.russian_federation = get(Geomodel, geonameid=2017370,
            name="Russian Federation",
            typ=GeoPlaceType.country,
            country_code="RU",
            parent=None)
        self.irkutsk = get(Geomodel, geonameid=7536078,
            name="Irkutsk",
            typ=GeoPlaceType.city,
            country_code="RU",
            parent=None)
        self.irkutsk_ru = u"Иркутск"
        get(Geoalternate, geoname=self.irkutsk,
            isolanguage='ru',
            variant=self.irkutsk_ru,
            preferred=1
            )
        get(Geoalternate, geoname=self.irkutsk,
            isolanguage='ru',
            variant=u"Иркуцк",
            preferred=0
            )
        self.irkutsk_pl = u"Irkuck"
        get(Geoalternate, geoname=self.irkutsk,
            isolanguage='pl',
            variant=self.irkutsk_pl,
            preferred=0
            )
        get(Geoalternate, geoname=self.russian_federation,
            isolanguage='ru',
            variant=u"Российская Федерация",
            preferred=1
            )

    def tearDown(self):
        utils.mongo_connection.drop_database('test_' + utils.mongo_settings['NAME'])
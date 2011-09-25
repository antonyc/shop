# -*- coding:utf-8 -*-
from catalog.models import Item, Category
import utils
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from pymongo import Connection
from geocoding.models import Geomodel, Geoalternate, GeoPlaceType
from orders.models import Delivery, StatusChoices, DeliveryTypes, Order, OrderStatuses, OrderItem
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
        self.setUpUsers()
        self.client.login(username='zver', password='1')


    def setUpUsers(self):
        self.user = User.objects.create_superuser('chapson', 'mrdark@yandex.ru', '1')
        self.user1 = User.objects.create_superuser('zver', 'anton@yandex.ru', '1')
        profile = self.user1.get_profile()
        profile.first_name = "Roman"
        profile.last_name = "Zver"
        profile.save()
        self.common_user = User.objects.create_user('common', 'chapson@yandex.ru.ru', '1')
        profile = self.common_user.get_profile()
        profile.first_name = "Coommon"
        profile.last_name = "User"
        profile.save()
        
    categories_set = False
    def setUpCategories(self):
        if self.categories_set:
            return
        self.categories_set = True
        self.for_woman = get(Category,
                             name="For woman",
                             url="woman",
                             parent=None)
        self.gifts = get(Category,
                         parent=self.for_woman,
                         name="Gifts for woman",
                         url="gifts")

    items_set = False
    def setUpItems(self):
        if self.items_set:
            return
        self.items_set = True
        self.setUpCategories()
        self.jewelry = get(Item, name="SexyJewelry",
                           description="jewelry",
                           url="jewelry",
                           hidden=False,
                           deleted=False,
                           price=120)
        self.toy = get(Item, name="Teddy Bear",
                       url="teddybear",
                       hidden=False,
                       deleted=False,
                       categories=[self.gifts],
                       price=3)

    deliveries_set = False
    def setUpDelivery(self):
        if self.deliveries_set:
            return
        self.deliveries_set = True
        self.delivery = get(Delivery,
                            ignore_fields=['dynamic_properties'],
                            name="Customer pickup",
                            status=StatusChoices.normal,
                            type=DeliveryTypes.shopper,
                            price=1,
                            description='')

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

    orders_set = False
    def setUpOrders(self):
        if self.orders_set:
            return
        self.setUpDelivery()
        self.setUpItems()
        self.zver_order = get(Order, user=self.user1,
                              status=OrderStatuses.new,
                              delivery=self.delivery)
        order_item = OrderItem(item=self.jewelry,
                               order=self.zver_order,
                               quantity=1,
                               price=120.21)
        order_item = get(OrderItem,
                         item=self.jewelry,
                         order=self.zver_order,
                         quantity=1,
                         price=120.21)
        order_item = get(OrderItem,
                         item=self.toy,
                         order=self.zver_order,
                         quantity=4,
                         price=1.99)
        
    def tearDown(self):
        utils.mongo_connection.drop_database('test_' + utils.mongo_settings['NAME'])
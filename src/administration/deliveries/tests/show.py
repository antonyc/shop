# -*- coding: utf-8 -*-

from django_dynamic_fixture import get
from django.core.urlresolvers import reverse
from orders.models import Delivery, DT_BY_SHOPPER
from utils.base_testcase import BaseTestCase
from django.contrib.auth.models import User

class DeliveriesShowTestCase(BaseTestCase):
    def setUp(self):
        super(DeliveriesShowTestCase, self).setUp()
        self.setGeoNames()
        self.delivery = get(Delivery, name="Self pick up",
                            description="Pick it up yourself",
                            type=DT_BY_SHOPPER,
                            price=0)
        self.delivery.dynamic_properties['address'] = {'text': {'country': self.russian_federation.geonameid,
                                                                'city': self.irkutsk.geonameid,
                                                                'street': u"Пугачева",
                                                                'building': "4а",
                                                                'office': "5",
                                                                "description": "Say the right name and get it free",
                                                                },
                                                       "point": {'lat': 52.16, 'lon': 104.17}
                                                       }
        self.client.login(username='chapson', password='1')
        
        
    def test_show_deliveries(self):
        self.client.logout()
        result = self.client.get(reverse('show_deliveries'))
        self.failIfEqual(result.status_code, 200, "This is not a correct request")

        self.client.login(username='chapson', password='1')
        result = self.client.get(reverse('show_deliveries'), **{'HTTP_ACCEPT_LANGUAGE': 'ru-ru'})
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")

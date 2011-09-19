# -*- coding:utf-8 -*-

from datetime import timedelta, datetime
from django.contrib.auth.models import User
from catalog.models import Item
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django_dynamic_fixture import get
from orders.models import Delivery, StatusChoices, DeliveryTypes
from utils.base_testcase import BaseTestCase

class CartTest(BaseTestCase):
    def setUp(self):
        super(CartTest, self).setUp()
        self.setUpDelivery()
        self.setUpItems()

    def test_empty(self):
        result = self.client.get(reverse('cart_show'))
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")

    def test_full(self):
        s = self.client.session
        s['cart'] = {'items': [{'url': self.jewelry.url,
                                                  'quantity': 1,
                                                  'added_at': datetime.now() - timedelta(days=2),
                                                  'price': 120},
                                                {'url': self.toy.url,
                                                 'quantity': 4,
                                                 'added_at': datetime.now() - timedelta(days=4),
                                                 'price': 3}],
                                       'price': 120+3*4,
                                       'total_price': 120+3*4+1,
                                       }
        s.save()
        result = self.client.get(reverse('cart_show'))
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")
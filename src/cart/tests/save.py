# -*- coding:utf-8 -*-

from django.contrib.auth.models import User
from catalog.models import Item
from django.core.urlresolvers import reverse
from django.utils import simplejson
from orders.models import Order
from utils.base_testcase import BaseTestCase

comment = u""" Captain, captain, smile!
        Cause your smile is the flag of the ship! """

class CartSaveTest(BaseTestCase):
    def setUp(self):
        super(CartSaveTest, self).setUp()
        self.setGeoNames()
        self.setUpDelivery()
        self.setUpItems()
        self.url = reverse('cart_show')
        self.correct_post = {'cart_item_id_' + str(self.jewelry.id): 2,
                             'cart_item_id_' + str(self.toy.id): 5,
                             'delivery_id': self.delivery.id,
                             'address-country__text': u"Россия",
                             'address-country': self.russian_federation.geonameid,
                             'address-city__text': u"Иркутск",
                             'address-city': self.irkutsk.geonameid,
                             'address-street': u"Пугачева",
                             'address-building': u"4",
                             "comment": comment
        }

    def test_save(self):
        counter = Order.objects.filter(user=self.user1)
        before = counter.count()
        response = self.client.post(self.url, self.correct_post)
        self.failUnlessEqual(response.status_code, 302, "This request must redirect to order page")
        self.failUnlessEqual(counter.count(), before + 1, "Must create 1 Order")
        order = counter.order_by('-id')[0]
        self.failUnlessEqual(order.orderitem_set.all().count(), 2, "Order must have 2 items")
        self.failUnlessEqual(order.delivery, self.delivery, "Delivery must be correct")
        order_jewelry = order.orderitem_set.get(item=self.jewelry)
        self.failUnlessEqual(order_jewelry.quantity, 2, "Must be 2 jewelry items")
        order_toy = order.orderitem_set.get(item=self.toy)
        self.failUnlessEqual(order_toy.quantity, 5, "Must be 5 toy items")
        self.failUnless(order.dynamic_properties.has_address(), "Order must have address")
        self.failUnless(order.dynamic_properties.has_text_address, "Order must have text address")
        self.failUnlessEqual(order.dynamic_properties['address']['text']['country__text'], u"Россия", "Must be correct country name")
        self.failUnlessEqual(order.dynamic_properties['address']['text']['city__text'], u"Иркутск", "Must be correct city name")

    def test_simple_bad_requests(self):
        counter = Order.objects.filter(user=self.user1)
        before = counter.count()
        response = self.client.post(self.url)
        self.failUnlessEqual(response.status_code, 200, "This request must show errors")
        self.failUnlessEqual(counter.count(), before, "Must not create order")

        self.client.logout()
        counter = Order.objects.filter(user=self.user1)
        before = counter.count()
        response = self.client.post(self.url, self.correct_post)
        self.failUnlessEqual(response.status_code, 302, "This request must redirect to login form")
        self.failUnlessEqual(counter.count(), before, "Must not create order")

    def test_missing_data_requests(self):
        counter = Order.objects.filter(user=self.user1)
        post = self.correct_post.copy()
        del post['cart_item_id_' + str(self.jewelry.id)]
        del post['cart_item_id_' + str(self.toy.id)]
        before = counter.count()
        response = self.client.post(self.url, post)
        self.failUnlessEqual(response.status_code, 200, "This request must show errors")
        self.failUnlessEqual(counter.count(), before, "Must not create order")

        post = self.correct_post.copy()
        del post['delivery_id']
        before = counter.count()
        response = self.client.post(self.url, post)
        self.failUnlessEqual(response.status_code, 200, "This request must show errors")
        self.failUnlessEqual(counter.count(), before, "Must not create order")

    def test_erroneous_data(self):
        counter = Order.objects.filter(user=self.user1)
        post = self.correct_post.copy()
        post['cart_item_id_4000'] = 1
        before = counter.count()
        response = self.client.post(self.url, post)
        self.failUnlessEqual(response.status_code, 200, "This request must show errors")
        self.failUnlessEqual(counter.count(), before, "Must not create order")

        counter = Order.objects.filter(user=self.user1)
        post = self.correct_post.copy()
        post['delivery_id'] = 10000
        before = counter.count()
        response = self.client.post(self.url, post)
        self.failUnlessEqual(response.status_code, 200, "This request must show errors")
        self.failUnlessEqual(counter.count(), before, "Must not create order")
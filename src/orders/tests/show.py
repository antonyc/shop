# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.utils import simplejson
from utils.base_testcase import BaseTestCase
from django_dynamic_fixture import get
from orders.models import Order, OrderItem, OrderStatuses

class ShowOrderTest(BaseTestCase):
    def setUp(self):
        super(ShowOrderTest, self).setUp()
        self.setGeoNames()
        self.setUpDelivery()
        self.setUpOrders()

    def test_show(self):
        url = reverse('view_order', kwargs={'id': self.zver_order.id})
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200, "A correct request")

    def test_as_other_user(self):
        self.client.login(username='common', password='1')
        url = reverse('view_order', kwargs={'id': self.zver_order.id})
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 403, "Cant view other peoples' orders")

    def test_as_admin(self):
        self.client.login(username='chapson', password='1')
        url = reverse('view_order', kwargs={'id': self.zver_order.id})
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200, "Can see as admin")

# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.utils import simplejson
from utils.base_testcase import BaseTestCase
from django_dynamic_fixture import get
from orders.models import Order, OrderItem, OrderStatuses, OrderComment

comment1 = """Hello! This order is great but can ya add 2 more books in it?!

Need them ''baaadly''
"""

class AddCommentTest(BaseTestCase):
    def setUp(self):
        super(AddCommentTest, self).setUp()
        self.setGeoNames()
        self.setUpDelivery()
        self.setUpOrders()

    def test_add(self):
        url = reverse('add_comment', kwargs={'id': self.zver_order.id})
        post = {'body': comment1}
        counter = OrderComment.objects.filter(user=self.user1, order=self.zver_order)
        before = counter.count()
        response = self.client.post(url, post)
        self.failUnlessEqual(response.status_code, 302, "A correct request which redirects")
        self.failUnlessEqual(counter.count(), before + 1, "Must have created 1 comment")

        url = reverse('view_order', kwargs={'id': self.zver_order.id})
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200, "A correct request")

    def test_empty(self):
        url = reverse('add_comment', kwargs={'id': self.zver_order.id})
        post = {'body': ''}
        counter = OrderComment.objects.filter(user=self.user1, order=self.zver_order)
        before = counter.count()
        response = self.client.post(url, post)
        self.failUnlessEqual(response.status_code, 302, "A redirect request")
        self.failUnlessEqual(counter.count(), before, "Must not have created a comment")

    def test_no_user(self):
        self.client.logout()
        url = reverse('add_comment', kwargs={'id': self.zver_order.id})
        post = {'body': comment1}
        response = self.client.post(url, post)
        self.failUnlessEqual(response.status_code, 403, "User must be logged in to use this")
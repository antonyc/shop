# -*- coding: utf-8 -*-
from django.test import TestCase
from catalog.models import Item
from django_dynamic_fixture import get
from orders.models import OrderItem, Order, NEW
from django.contrib.auth.models import User
from orders.models import DELETED

class StatusOrdersTest(TestCase):
    fixtures = ['categories.json']
    def setUp(self):
        self.user = get(User, username='chapson')
        items = Item.objects.all()[:2]
        self.order = get(Order, user=self.user, status=NEW)
        self.orders_item = []
        self.user = User.objects.create_superuser('zver', 'anton.chaporgin@list.ru', '1')
        self.client.login(username='zver', password='1')
        for item in items:
            self.orders_item.append(get(OrderItem,item=item,
                order=self.order,
                quantity=2))
    
    def test_delete_order(self):
        before_orders = Order.objects.all().count()
        result = self.client.post('/administration/orders/%d/status/' % self.order.id, {'status': DELETED,})
        self.failUnlessEqual(result.status_code, 302, "This is a correct request which redirects")
        after_orders = Order.objects.all().count()
#        print before_orders - 1, after_orders
#        print Order.objects.all()[0].status
        self.failUnlessEqual(before_orders - 1, after_orders, "Must have deleted 1 order")

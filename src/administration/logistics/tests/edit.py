# -*- coding: utf-8 -*-
from django.test import TestCase
from catalog.models import Item, Category
from django.http import QueryDict
from django_dynamic_fixture import get
from utils.strings import translit
from orders.models import OrderItem, Order, NEW
from django.contrib.auth.models import User

class EditOrderTest(TestCase):
    fixtures = ['categories.json']
    def setUp(self):
        self.user = get(User, username='chapson')
        items = Item.objects.all()[:2]
        self.order = get(Order, user=self.user, status=NEW)
        self.orders_item = []
        for item in items:
            self.orders_item.append(get(OrderItem,item=item,
                order=self.order,
                quantity=2))
        
        
    def test_edit_order(self):
        result = self.client.get('/administration/orders/%d/edit/' % self.order.id)
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")
        
    def test_edit_order_item(self):
        post = {'quantity': 10}
        result = self.client.post('/administration/orders/item/%d/edit/' % self.orders_item[0].id, post)
        self.failUnlessEqual(result.status_code, 302, "This is a correct request which redirects")
        order_item = OrderItem.objects.get(id=self.orders_item[0].id)
        self.failUnlessEqual(order_item.quantity, 10, "Must change quantity")

    def test_delete_order_item(self):
        result = self.client.post('/administration/orders/item/%d/delete/' % self.orders_item[0].id)
        self.failUnlessEqual(result.status_code, 302, "This is a correct request which redirects")
        order_items = OrderItem.objects.filter(id=self.orders_item[0].id).count()
        self.failUnlessEqual(order_items, 0, "Must have deleted order item")
        
    def test_edit_order_item_AJAX(self):
        post = {'quantity': 10}
        result = self.client.post('/administration/orders/item/%d/edit/' % self.orders_item[0].id, post,
                                  **{'X-Requested-With': 'XMLHttpRequest'})
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")
        order_item = OrderItem.objects.get(id=self.orders_item[0].id)
        self.failUnlessEqual(order_item.quantity, 10, "Must change quantity")

    def test_delete_order_item_AJAX(self):
        result = self.client.post('/administration/orders/item/%d/delete/' % self.orders_item[0].id,
                                  **{'X-Requested-With': 'XMLHttpRequest'})
        self.failUnlessEqual(result.status_code, 200, "This is a correct request which redirects")
        order_items = OrderItem.objects.filter(id=self.orders_item[0].id).count()
        self.failUnlessEqual(order_items, 0, "Must have deleted order item")
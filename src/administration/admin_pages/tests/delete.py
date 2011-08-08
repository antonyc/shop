# -*- coding: utf-8 -*-
from django.test import TestCase
from catalog.models import Item
from django_dynamic_fixture import get
from orders.models import OrderItem, Order, NEW
from django.contrib.auth.models import User
from orders.models import DELETED

class DeletePageTest(TestCase):
    fixtures = ['categories.json']
    def setUp(self):
        self.user = User.objects.create_superuser('chapson', 'mrdark@list.ru', '1')
        self.client.login(username='chapson', password='1')
        self.user = User.objects.create_superuser('chapson', 'mrdark@list.ru', '1')
        self.user1 = User.objects.create_superuser('zver', 'anton@list.ru', '1')
        self.client.login(username='chapson', password='1')

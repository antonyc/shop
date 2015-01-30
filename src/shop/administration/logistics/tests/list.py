# -*- coding: utf-8 -*-
from django.test import TestCase
from catalog.models import Item
from django.contrib.auth.models import User

class ListOrdersTest(TestCase):
    fixtures = ['categories.json']
    def setUp(self):
        self.user = User.objects.create_superuser('chapson', 'mrdark@list.ru', '1')
        self.client.login(username='chapson', password='1')
    
    def test_list_items(self):
        result = self.client.get('/administration/orders/')
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")

# -*- coding: utf-8 -*-
from django.test import TestCase
from catalog.models import Item
'''
Created on 31.07.2011

@author: chapson
'''
from django.contrib.auth.models import User

class ListItemTest(TestCase):
    fixtures = ['categories.json']
    def setUp(self):
        self.user = User.objects.create_superuser('chapson', 'mrdark@list.ru', '1')
        self.user1 = User.objects.create_superuser('zver', 'anton@list.ru', '1')
        self.client.login(username='chapson', password='1')
    
    def test_list_items(self):
        result = self.client.get('/administration/items/')
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")
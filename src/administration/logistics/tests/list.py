# -*- coding: utf-8 -*-
from django.test import TestCase
from catalog.models import Item
'''
Created on 31.07.2011

@author: chapson
'''

class DeleteOrdersTest(TestCase):
    fixtures = ['categories.json']
    def setUp(self):
        pass
    
    def test_list_items(self):
        result = self.client.get('/administration/orders/')
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")

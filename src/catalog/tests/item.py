# -*- coding: utf-8 -*-
from django.test import TestCase
from django_dynamic_fixture import new
from catalog.models import Item
'''
Created on 31.07.2011

@author: chapson
'''

class AdminItemTest(TestCase):
    fixtures = ['categories.json']
    def setUp(self):
        pass
    
    def test_list_items(self):
        pass

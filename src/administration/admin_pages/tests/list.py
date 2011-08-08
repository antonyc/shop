# -*- coding: utf-8 -*-
from django.test import TestCase
from catalog.models import Item
'''
Created on 31.07.2011

@author: chapson
'''
from django.contrib.auth.models import User

class ListPagesTest(TestCase):
    fixtures = ['categories.json']
    def setUp(self):
        self.user = User.objects.create_superuser('chapson', 'mrdark@list.ru', '1')
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username='chapson', password='1')
    
    def test_list_page(self):
        result = self.client.get('/administration/pages/')
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")

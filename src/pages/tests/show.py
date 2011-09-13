# -*- coding: utf-8 -*-
'''
Created on 08.08.2011

@author: chapson
'''
from django.test import TestCase
from catalog.models import Item, Category
from django.http import QueryDict
from django_dynamic_fixture import get
from utils.strings import translit
from orders.models import OrderItem, Order, NEW
from django.contrib.auth.models import User
from administration.admin_pages.tests.parser import BODY_LINKED
from pages.models import Page
from django.core.urlresolvers import reverse


class ShowPageTest(TestCase):
    fixtures = ['categories.json']
    def setUp(self):
        post = {'body': BODY_LINKED, 
                'title': 'Супер страница',
                }
        self.user = User.objects.create_superuser('zver', 'anton@list.ru', '1')
        self.client.login(username='zver', password='1')
        result = self.client.post('/administration/pages/add/', post)
        self.page = Page.objects.all()[0]
        
    def test_show(self):
        result = self.client.get(reverse('show_page', kwargs={'url': self.page.url}))
        self.failUnlessEqual(result.status_code, 200, "Must be a correct request")
        
    def test_double_redirect(self):
        pass
        
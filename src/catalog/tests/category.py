# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_dynamic_fixture import new
from catalog.models import Item
from utils.base_testcase import BaseTestCase

class ShowCategory(BaseTestCase):
    def setUp(self):
        super(ShowCategory, self).setUp()
        self.setUpItems()

    def test_show(self):
        url = reverse('show_category', kwargs={'url': self.for_woman.url+'/'+self.gifts.url})
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200, "This is a correct request")
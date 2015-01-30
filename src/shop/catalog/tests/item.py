# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_dynamic_fixture import new
from catalog.models import Item
from utils.base_testcase import BaseTestCase

class ShowItem(BaseTestCase):
    def setUp(self):
        super(ShowItem, self).setUp()
        self.setUpItems()

    def test_show(self):
        url = reverse('show_item', kwargs={'url': self.toy.url})
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200, "This is a correct request")
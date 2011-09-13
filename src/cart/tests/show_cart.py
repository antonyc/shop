# -*- coding:utf-8 -*-

from django.contrib.auth.models import User
from catalog.models import Item
from django.core.urlresolvers import reverse
from django.utils import simplejson
from utils.base_testcase import BaseTestCase

class CartTest(BaseTestCase):
    def test_show(self):
        result = self.client.get(reverse('cart_show'))
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")
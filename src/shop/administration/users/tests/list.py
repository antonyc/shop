# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from catalog.models import Item
from django.contrib.auth.models import User
from utils.base_testcase import BaseTestCase


class ListUsersTest(BaseTestCase):
    def test_list_users(self):
        result = self.client.get(reverse('list_users'))
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")
        self.failUnless('Zver' in result.content, "Must have chapson username in content")

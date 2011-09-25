# -*- coding: utf-8 -*-
__author__ = 'chapson'
from django.core.urlresolvers import reverse
from administration.admin_pages.tests.edit import BODY
from utils import site_settings
from django.test import TestCase
from django_dynamic_fixture import get
from utils.base_testcase import BaseTestCase
top_menu = """
[[страничка1|Зайди на меня]] [[jewelry|Драгоценность]]
http://music.yandex.ru/#!/artist/15791
"""


class EditSettingsTest(BaseTestCase):
    def setUp(self):
        super(EditSettingsTest, self).setUp()
        self.setUpItems()

    def setUpPages(self):
        title = u"страничка1"
        post = {'body': BODY, 'title': title}
        self.client.post(reverse('add_page'), post)

    def test_show_settings(self):
        response = self.client.get(reverse('show_settings'))
        self.failUnlessEqual(response.status_code, 200, "A correct request")

    def test_save_settings(self):
        post = {'top_menu': top_menu}
        response = self.client.post(reverse('show_settings'), post)
        self.failUnlessEqual(response.status_code, 302, "This is a redirect")
# -*- coding: utf-8 -*-
'''
Created on 08.08.2011

@author: chapson
'''
import os
from datetime import datetime, timedelta
from pages.models import Page
from django.contrib.auth.models import User
from utils.base_testcase import BaseTestCase
from django.core.management import call_command


class SitemapTest(BaseTestCase):
    def setUp(self):
        super(SitemapTest, self).setUp()
        page = Page(author=self.user,
                    url="mobydick/chapter1",
                    body="",
                    formatted_body="",
                    title="")
        page.save()

    def test_generate(self):
        """Generate XML with present pages"""
        
        path = '/tmp/sitemap.xml'
        if os.path.exists(path):
            os.unlink(path)
        self.assertTrue(not os.path.exists(path), "Must have deleted sitemap")
        call_command('sitemap', verbosity=2, pages=0, output=path)
        self.assertTrue(os.path.exists(path), "Must have created sitemap")


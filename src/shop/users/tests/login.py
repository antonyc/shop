# -*- coding: utf-8 -*-
'''
Created on 08.08.2011

@author: chapson
'''

from django.test import TestCase


class LoginTest(TestCase):
    def test_login(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

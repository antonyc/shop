# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from catalog.models import Item
from django.contrib.auth.models import User
from utils.base_testcase import BaseTestCase

first_name = 'Arnold'
last_name = 'Schwartznegger'
email = 'chaporginanton@yandex.ru'


class EditShowUserTest(BaseTestCase):
    def test_show_user(self):
        chapson = User.objects.get(username='chapson')
        result = self.client.get(reverse('show_user', kwargs={'id': chapson.id}))
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")

    def test_edit_user(self):
        chapson = User.objects.get(username='chapson')
        result = self.client.get(reverse('edit_user', kwargs={'id': chapson.id}))
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")

    def test_save_existing_user(self):
#        print "test_save_existing_user"
        chapson = User.objects.get(username='chapson')
        post = {'ui_lang': 'en',
                'username': chapson.username,
                'first_name': first_name,
                'last_name': last_name,
                'email': email}
        result = self.client.post(reverse('edit_user', kwargs={'id': chapson.id}),
                                  post)
#        print result
        self.assertEquals(result.status_code, 302, "Must redirect")
        chapson = User.objects.get(username='chapson')
        profile = chapson.get_profile()
        self.assertEqual(profile.first_name, first_name)
        self.assertEqual(profile.last_name, last_name)
        self.assertEqual(chapson.email, email)
        self.assertEqual(profile.ui_lang, 'en')

    def test_incorrect_save(self):
        chapson = User.objects.get(username='chapson')
        post = {'ui_lang': 'en',
                'first_name': first_name,
                'last_name': last_name,
                'email': ''}
        result = self.client.post(reverse('edit_user', kwargs={'id': chapson.id}),
                                  post)
        self.assertEquals(result.status_code, 200)
        chapson = User.objects.get(username='chapson')
        profile = chapson.get_profile()
        self.assertNotEqual(profile.first_name, first_name)
        self.assertNotEqual(profile.last_name, last_name)
        self.assertNotEqual(chapson.email, '')
        self.assertNotEqual(profile.ui_lang, 'en')

    def test_add_user(self):
        chapson = User.objects.get(username='chapson')
        url = reverse('add_user')
        result = self.client.get(url)
        self.assertEqual(result.status_code, 200, "A correct request")
        post = {'ui_lang': 'en',
                'username': 'chaporginanton',
                'first_name': first_name,
                'last_name': last_name,
                'email': chapson.email}
        counter = User.objects.all()
        before = counter.count()
        result = self.client.post(url, post)
        self.assertEqual(result.status_code, 200, "Must show form again")
        self.assertEqual(before, counter.count(), "Must not add user")
        post['email'] = 'chaporginanton@yandex.ru'
        result = self.client.post(url, post)
        self.assertEqual(result.status_code, 302, "Must redirect")
        self.assertEqual(before + 1, counter.count(), "Must have added user")
        canton = User.objects.get(email='chaporginanton@yandex.ru')

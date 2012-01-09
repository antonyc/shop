# -*- coding: utf-8 -*-
import administration
import os
from django.test import TestCase
from pages.models import Page, PageImage
from django.utils import simplejson
from django.contrib.auth.models import User
from utils.strings import parse_markup
add_url = '/administration/pages/%d/images/add/'


class PageImageUploadTest(TestCase):
    fixtures = ['categories.json']
    def setUp(self):
        self.user = User.objects.create_superuser('chapson', 'mrdark@list.ru', '1')
        self.page = Page(title="a page",
             body="",
             url="a-cosmic-ship",
             author=self.user)
        self.page.save()
        self.file_path = os.path.join(os.path.dirname(administration.__file__), 'fixtures')
        self.user1 = User.objects.create_superuser('zver', 'anton@list.ru', '1')
        self.client.login(username='chapson', password='1')

    def upload_file(self):
        fp = open(os.path.join(self.file_path, '1.jpg'))
#        f = self.client.encode_file(self.client.MULTIPART_CONTENT, 'image', fp)
#        fp.close()
        before_images = PageImage.objects.filter(page=self.page).count()
        alt = u'Мишка на севере'
        post = {'image': fp, 'alt': alt,}
        result = self.client.post(add_url % self.page.id, post)
        fp.close()
        return result

    def test_usual_request(self):
        result = self.upload_file()
        self.failUnlessEqual(result.status_code, 302, "This is a correct request which redirects")

    def test_markup(self):
        self.test_usual_request()
        self.test_usual_request()
        ids = map(lambda i: str(i.id), PageImage.objects.all())
        body = parse_markup("Hello. \n\n=== Hello \n\n aaa \n\n <<images " + ", ".join(ids) + " >>")
        self.assertTrue("page_images" in body)
        self.assertTrue("user_uploads" in body)

    def test_post(self):
        fp = open(os.path.join(self.file_path, '1.jpg'))
        before_images = PageImage.objects.filter(page=self.page).count()
        alt = u'Мишка на севере'
        post = {'image': fp, 'alt': alt,}
        result = self.client.post(add_url % self.page.id, post,
                                  **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        fp.close()
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")
        after_images = PageImage.objects.filter(page=self.page).count()
        self.assertEqual(before_images + 1, after_images, "Must have added image")
        json = simplejson.loads(result.content)
        page_image = PageImage.objects.get(id=json['id'])
        self.failUnlessEqual(page_image.alt, alt, "Alt must be the same as it was specified in request")
        self.failUnlessEqual(page_image.page, self.page, "Must be the specified page")
        
        fp = open(os.path.join(self.file_path, '1.jpg'))
        post = {'image': fp, 'alt': '',}
        result = self.client.post(add_url % self.page.id, post)
        fp.close()
        self.failUnlessEqual(result.status_code, 409, "Must be a conflict request")
        json = simplejson.loads(result.content)
        self.failUnless('fields' in json, "Must be error in JSON")
        self.failUnless('alt' in json['fields'], "Must be error about alt")

        # post without image
        post = {'alt': 'Some alt',}
        result = self.client.post(add_url % self.page.id, post)
        self.assertEqual(result.status_code, 409, "Must be a conflict request")
        json = simplejson.loads(result.content)
        self.assertTrue('fields' in json, "Must be error in JSON")
        self.assertTrue('image' in json['fields'], "Must be error about image")
        
        fp = open(os.path.join(self.file_path, '1.jpg'))
        post = {'image': fp, 'alt': 'Some alt',}
        result = self.client.post(add_url % 1000, post)
        fp.close()
        self.failUnlessEqual(result.status_code, 404, "Must be a 404 response")
        
    def test_upload_incorrect_file(self):
        fp = open(os.path.join(self.file_path, 'swfobject.js'))
#        f = self.client.encode_file(self.client.MULTIPART_CONTENT, 'image', fp)
#        fp.close()
        alt = u'Мишка на севере'
        post = {'image': fp, 'alt': alt,}
        before_images = PageImage.objects.filter(page=self.page).count()
        result = self.client.post(add_url % self.page.id, post)
        fp.close()
        self.failUnlessEqual(result.status_code, 409, "Must be a conflict request")
        json = simplejson.loads(result.content)
        self.failUnless('fields' in json, "Must be error in JSON")
        self.failUnless('image' in json['fields'], "Must be error about item")
        after_images = PageImage.objects.filter(page=self.page).count()
        self.failUnlessEqual(before_images, after_images, "Images must not have been added")
        

DESCRIPTION_1 = u"""
Покупайте этот <ul>телефон</ul>.
Он хороший и ''новый''
"""
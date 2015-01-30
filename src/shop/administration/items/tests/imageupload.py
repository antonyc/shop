# -*- coding: utf-8 -*-
import administration
import os
from django.test import TestCase
from catalog.models import Item, Category, ItemImage
from django.utils import simplejson
from django.contrib.auth.models import User

class ItemImageUploadTest(TestCase):
    fixtures = ['categories.json']
    def setUp(self):
        self.item = Item(name="A cosmic ship",
             description=DESCRIPTION_1,
             url="a-cosmic-ship",
             price=20)
        self.item.save()
        self.item.categories = Category.objects.all()[:2]
        self.item.save()
        self.file_path = os.path.join(os.path.dirname(administration.__file__), 'fixtures')
        self.user = User.objects.create_superuser('chapson', 'mrdark@list.ru', '1')
        self.user1 = User.objects.create_superuser('zver', 'anton@list.ru', '1')
        self.client.login(username='chapson', password='1')

    def test_usual_request(self):
        fp = open(os.path.join(self.file_path, '1.jpg'))
#        f = self.client.encode_file(self.client.MULTIPART_CONTENT, 'image', fp)
#        fp.close()
        before_images = ItemImage.objects.filter(item=self.item).count()
        alt = u'Мишка на севере'
        post = {'image': fp, 'alt': alt,}
        result = self.client.post('/administration/items/%d/images/add/' % self.item.id, post)
        fp.close()
        self.failUnlessEqual(result.status_code, 302, "This is a correct request which redirects")
    
    def test_post(self):
        fp = open(os.path.join(self.file_path, '1.jpg'))
#        f = self.client.encode_file(self.client.MULTIPART_CONTENT, 'image', fp)
#        fp.close()
        before_images = ItemImage.objects.filter(item=self.item).count()
        alt = u'Мишка на севере'
        post = {'image': fp, 'alt': alt,}
        result = self.client.post('/administration/items/%d/images/add/' % self.item.id, post,
                                  **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        fp.close()
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")
        after_images = ItemImage.objects.filter(item=self.item).count()
        self.failUnlessEqual(before_images + 1, after_images, "Must have added item")
        json = simplejson.loads(result.content)
        item_image = ItemImage.objects.get(id=json['id'])
        self.failUnlessEqual(item_image.alt, alt, "Alt must be the same as it was specified in request")
        self.failUnlessEqual(item_image.item, self.item, "Must be the specified item")
        
        fp = open(os.path.join(self.file_path, '1.jpg'))
        post = {'image': fp, 'alt': '',}
        result = self.client.post('/administration/items/%d/images/add/' % self.item.id, post)
        fp.close()
        self.failUnlessEqual(result.status_code, 409, "Must be a conflict request")
        json = simplejson.loads(result.content)
        self.failUnless('fields' in json, "Must be error in JSON")
        self.failUnless('alt' in json['fields'], "Must be error about alt")
        
        post = {'alt': 'Some alt',}
        result = self.client.post('/administration/items/%d/images/add/' % self.item.id, post)
        self.failUnlessEqual(result.status_code, 409, "Must be a conflict request")
        json = simplejson.loads(result.content)
        self.failUnless('fields' in json, "Must be error in JSON")
        self.failUnless('image' in json['fields'], "Must be error about image")
        
        fp = open(os.path.join(self.file_path, '1.jpg'))
        post = {'image': fp, 'alt': 'Some alt',}
        result = self.client.post('/administration/items/%d/images/add/' % 1000, post)
        fp.close()
        self.failUnlessEqual(result.status_code, 404, "Must be a 404 response")
        
    def test_upload_incorrect_file(self):
        fp = open(os.path.join(self.file_path, 'swfobject.js'))
#        f = self.client.encode_file(self.client.MULTIPART_CONTENT, 'image', fp)
#        fp.close()
        alt = u'Мишка на севере'
        post = {'image': fp, 'alt': alt,}
        before_images = ItemImage.objects.filter(item=self.item).count()
        result = self.client.post('/administration/items/%d/images/add/' % self.item.id, post)
        fp.close()
        self.failUnlessEqual(result.status_code, 409, "Must be a conflict request")
        json = simplejson.loads(result.content)
        self.failUnless('fields' in json, "Must be error in JSON")
        self.failUnless('image' in json['fields'], "Must be error about item")
        after_images = ItemImage.objects.filter(item=self.item).count()
        self.failUnlessEqual(before_images, after_images, "Images must not have been added")
        
    
DESCRIPTION_1 = u"""
Покупайте этот <ul>телефон</ul>.
Он хороший и ''новый''
"""
# -*- coding: utf-8 -*-
import administration
import os
from django_dynamic_fixture import get
from django.test import TestCase
from catalog.models import Item, Category, ItemImage
from django.utils import simplejson
from django.contrib.auth.models import User

class ItemImageDeleteTest(TestCase):
    fixtures = ['categories.json']
    def setUp(self):
        self.item = get(Item, name="A cosmic ship",
             description=DESCRIPTION_1,
             url="a-cosmic-ship")
        self.item.save()
        self.item.categories = Category.objects.all()[:2]
        self.item.save()
        self.file_path = os.path.join(os.path.dirname(administration.__file__), 'fixtures')
        self.user = User.objects.create_superuser('chapson', 'mrdark@list.ru', '1')
        self.user1 = User.objects.create_superuser('zver', 'anton@list.ru', '1')
        self.client.login(username='chapson', password='1')

    def test_delete(self):
        fp = open(os.path.join(self.file_path, '1.jpg'))
        before_images = ItemImage.objects.filter(item=self.item).count()
        alt = u'Мишка на севере'
        post = {'image': fp, 'alt': alt,}
        result = self.client.post('/administration/items/%d/images/add/' % self.item.id, post)
        fp.close()
        self.failUnlessEqual(result.status_code, 302, "This is a correct request which redirects")
        after_images = ItemImage.objects.filter(item=self.item).count()
        self.failUnlessEqual(before_images + 1, after_images, "Must have added images")
        image = ItemImage.objects.filter(item=self.item)[before_images]
        before_images = ItemImage.objects.filter(item=self.item).count()
        result = self.client.post('/administration/items/images/%d/delete/' % image.id, {})
        self.failUnlessEqual(result.status_code, 302, "This is a correct request which redirects")
        after_images = ItemImage.objects.filter(item=self.item).count()
        self.failUnlessEqual(before_images - 1, after_images, "Must have deleted one item")
     
DESCRIPTION_1 = u"""
Покупайте этот <ul>телефон</ul>.
Он хороший и ''новый''
"""
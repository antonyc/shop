# -*- coding: utf-8 -*-
from django_dynamic_fixture import get
from django.test import TestCase
from catalog.models import Item, Category
from django.contrib.auth.models import User

class DeleteCategoryTest(TestCase):
    fixtures = ['categories.json']
    def setUp(self):
        self.item = get(Item, name="A cosmic ship",
             description=DESCRIPTION_1,
             url="a-cosmic-ship")
        self.item.save()
        self.item.categories = Category.objects.all()[:4]
        self.item.save()
        self.user = User.objects.create_superuser('chapson', 'mrdark@list.ru', '1')
        self.user1 = User.objects.create_superuser('zver', 'anton@list.ru', '1')
        self.client.login(username='chapson', password='1')
    
    def test_get(self):
        result = self.client.get('/administration/items/%d/delete/' % self.item.id)
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")
    
    def test_post(self):
        result = self.client.post('/administration/items/%d/delete/' % self.item.id)
        self.failUnlessEqual(result.status_code, 302, "This is a correct request, which redirects")
        self.failUnlessEqual(Item.public_objects.filter(id=self.item.id).count(), 0, "Must have deleted item")
        
DESCRIPTION_1 = u"""
Покупайте этот <ul>телефон</ul>.
Он хороший и ''новый''
"""
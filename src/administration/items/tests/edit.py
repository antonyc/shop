# -*- coding: utf-8 -*-
from django_dynamic_fixture import get
from django.test import TestCase
from catalog.models import Item, Category
from django.http import QueryDict
from utils.strings import translit
from django.contrib.auth.models import User

class EditItemTest(TestCase):
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
    
    def test_create_item(self):
        result = self.client.get('/administration/items/add/')
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")
        
        before_items = int(Item.objects.count())
        result = self.client.post('/administration/items/add/', {'name': u'Новый телефон', 
                                                                 'description': DESCRIPTION_1,
                                                                 'price': 200.12
                                                                 })
        self.failUnlessEqual(result.status_code, 302, "This is a correct request, which redirects")
        after_items = Item.objects.count()
        self.failUnlessEqual(before_items+1, after_items, "Must have added 1 Item")
        created = Item.objects.all()[before_items]
        self.failUnlessEqual(created.url, translit(created.name).lower(), "Must have transliterated URL")
        self.failUnlessEqual(created.price, 200.12, "Must have changed price")
        
        before_items = int(Item.objects.count())
        post = QueryDict(None, mutable = True)
        post['name'] = u'Новый телефон'
        post['description'] = DESCRIPTION_1
        cats = Category.objects.all()[:1]
        post['categories'] = map(lambda c: c.id, cats)
        post['price'] = 120
        result = self.client.post('/administration/items/add/', post)
        self.failUnlessEqual(result.status_code, 302, "This is a correct request, which redirects")
        after_items = Item.objects.count()
        self.failUnlessEqual(before_items+1, after_items, "Must have added 1 Item")
        
    def test_edit_item(self):
        item = Item.objects.all()[0]
        request = '/administration/items/%d/edit/' % item.id
        result = self.client.get(request)
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")
        
        request = '/administration/items/%d/edit/' % item.id
        post = QueryDict(None, mutable = True)
        name = u'Новый супер пупер граммофон'
        post['name'] = name
        description = "supa description"
        post['description'] = description
        post['categories'] = map(lambda c: c.id, Category.objects.all()[:1])
        post['price'] = 400
        result = self.client.post(request, post)
        self.failUnlessEqual(result.status_code, 302, "This is a correct request, which redirects")
        updated_item = Item.objects.get(id=item.id)
        self.failUnlessEqual(updated_item.url, item.url, "Must not change url")
        self.failUnlessEqual(name, updated_item.name, "Name must have changed")
        self.failUnlessEqual(updated_item.price, 400, "Must have changed price")
        self.failUnlessEqual(1, len(updated_item.categories.all()), "Must be 1 category")
        self.failUnlessEqual(description, updated_item.description, "Description must have changed")
        
        post = QueryDict(None, mutable = True)
        post['name'] = ''
        post['description'] = description
        post['categories'] = []
        result = self.client.post(request, post)
        self.failUnlessEqual(result.status_code, 409, "This is conflict request")
        
        post = QueryDict(None, mutable = True)
        post['name'] = 'not empty'
        post['description'] = ''
        post['categories'] = []
        result = self.client.post(request, post)
        self.failUnlessEqual(result.status_code, 409, "This is conflict request")
    
DESCRIPTION_1 = u"""
Покупайте этот <ul>телефон</ul>.
Он хороший и ''новый''
"""
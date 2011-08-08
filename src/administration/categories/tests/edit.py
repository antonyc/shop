# -*- coding: utf-8 -*-
from django.test import TestCase
from catalog.models import Item, Category
from django.http import QueryDict
from utils.strings import translit
from django.contrib.auth.models import User

class EditCategoryTest(TestCase):
    fixtures = ['categories.json']
    def setUp(self):
        self.category = Category(name=u"Промышленные товары 2",
                             url="promtovary2")
        self.category.save()
        self.cat1 = Category(name=u"Телки-Метелки",
                             url="telkimetelki",
                             parent=self.category)
        self.cat1.save()
        self.user = User.objects.create_superuser('chapson', 'mrdark@list.ru', '1')
        self.user1 = User.objects.create_superuser('zver', 'anton@list.ru', '1')
        self.client.login(username='chapson', password='1')
        
    def test_create_category(self):
        result = self.client.get('/administration/categories/add/')
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")
        
        before_items = int(Category.objects.count())
        vantuzy = u'Шланги'
        parent = Category.objects.get(id=1)
        result = self.client.post('/administration/categories/add/', {'name': vantuzy, 
                                                                      'parent': parent.id,
                                                                      })
        self.failUnlessEqual(result.status_code, 302, "This is a correct request, which redirects")
        after_items = Category.objects.count()
        self.failUnlessEqual(before_items+1, after_items, "Must have added 1 Category")
        created = Category.objects.all()[before_items]
        self.failUnlessEqual(created.url, translit(created.name).lower(), "Must have transliterated URL")
        self.failUnlessEqual(created.parent, parent, "Must have 'promtovary' as a parent")
        self.failUnlessEqual(created.name, vantuzy, "Must set name")
        
        before_items = int(Category.objects.count())
        result = self.client.post('/administration/categories/add/', {'name': ''})
        self.failUnlessEqual(result.status_code, 409, "This is a conflict request")
        after_items = Category.objects.count()
        self.failUnlessEqual(before_items, after_items, "Must not have added an Item")
        
        before_items = int(Category.objects.count())
        result = self.client.post('/administration/categories/add/', {'name': vantuzy,
                                                                      })
        self.failUnlessEqual(result.status_code, 302, "This is a correct request, which redirects")
        after_items = Category.objects.count()
        self.failUnlessEqual(before_items+1, after_items, "Must have added 1 Item")

    def test_edit_category(self):
        request = '/administration/categories/%d/edit/' % self.cat1.id
        result = self.client.get(request)
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")
        
        request = '/administration/categories/%d/edit/' % self.category.id
        name = u'Пылесосы'
        result = self.client.post(request, {'name': name,
                                            })
        self.failUnlessEqual(result.status_code, 302, "This is a correct request, which redirects")
        updated_category = Category.objects.get(id=self.category.id)
        self.failUnlessEqual(updated_category.url, self.category.url, "Must not change url")
        self.failUnlessEqual(name, updated_category.name, "Name must have changed")
        self.failUnlessEqual(updated_category.parent, None, "Must be 1 category")
        
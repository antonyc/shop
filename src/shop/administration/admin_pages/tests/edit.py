# -*- coding: utf-8 -*-
from django.test import TestCase
from catalog.models import Item, Category
from django.http import QueryDict
from django_dynamic_fixture import get
from utils.strings import translit
from orders.models import OrderItem, Order, NEW
from django.contrib.auth.models import User
from pages.models import Page, RedirectPage

class EditPageTest(TestCase):
    fixtures = ['categories.json']
    def setUp(self):
        self.user = User.objects.create_superuser('chapson', 'mrdark@list.ru', '1')
        self.user1 = User.objects.create_superuser('zver', 'anton@list.ru', '1')
        self.client.login(username='chapson', password='1')

    def test_add_page(self):
        result = self.client.get('/administration/pages/add/')
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")
        
        title = u"Новая супер страница!"
        post = {'body': BODY, 'title': title}
        result = self.client.post('/administration/pages/add/', post)
        self.failUnlessEqual(result.status_code, 302, "A correct request which redirects")
        self.failUnlessEqual(Page.objects.filter(url=translit(title)).count(), 1, "Must have created page")
        page = Page.objects.get(url=translit(title))
        self.failUnless(page.formatted_body, "Must have filled formatted body")
        self.failUnlessEqual(self.user, page.author, "The author must be chapson")
        self.failUnlessEqual(self.user.username, page.last_user, "The last_user must be chapson")
        
        title = u"Новая супер страница"
        post = {'body': BODY, 'title': title}
        result = self.client.post('/administration/pages/add/', post)
        self.failUnlessEqual(result.status_code, 302, "A correct request which redirects")
        
    def test_edit_nonexistent_page(self):
        result = self.client.get('/administration/pages/%d/edit/' % 100)
        self.failUnlessEqual(result.status_code, 404, "Must be a 404")
        
    def test_edit_page_title(self):
        title = u"Новая супер страница"
        post = {'body': BODY, 'title': title}
        result = self.client.post('/administration/pages/add/', post)
        old_page = Page.objects.get(url=translit(title))
        
        result = self.client.get('/administration/pages/%d/edit/' % old_page.id)
        self.failUnlessEqual(result.status_code, 200, "A correct request to existing page")
        
        #login!
        self.client.login(username='zver', password='1')
        result = self.client.get('/administration/pages/%d/edit/' % old_page.id)
        self.failUnlessEqual(result.status_code, 200, "A correct request to existing page")
        
        title = u"Изменяю заголовок"
        post = {'body': BODY, 'title': title}
        before_redirects = RedirectPage.objects.all().count()
        import time
        time.sleep(2)
        result = self.client.post('/administration/pages/%d/edit/' % old_page.id, post)
        self.failUnlessEqual(result.status_code, 302, "A correct request which redirects")
        renewed_page = Page.objects.get(id=old_page.id)
        self.failIfEqual(renewed_page.title, old_page.title, "Must have changed title")
        self.failUnlessEqual(renewed_page.author, old_page.author, "Author must stay the same")
        self.failUnless(renewed_page.updated_at > old_page.updated_at, "Must have changed 'updated_at'")
        self.failUnlessEqual(renewed_page.last_user, 'zver', "Must have changed 'last_user'")
        self.failIfEqual(renewed_page.url, old_page.url, "Must have changed title")
        after_redirects = RedirectPage.objects.all().count()
        self.failUnlessEqual(before_redirects + 1, after_redirects, "Must have added 1 redirect")
        redirect = RedirectPage.objects.get(from_url=old_page.url)
        self.failUnlessEqual(redirect.to_page, renewed_page, "Redirect must lead to URL of new page")

BODY = u"""
=== заголовок ===
[[new page]]

какой то текст!
еще
немного

==== заголовок 2 ====
все
"""
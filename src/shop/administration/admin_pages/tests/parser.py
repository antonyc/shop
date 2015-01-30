# -*- coding: utf-8 -*-
from django.test import TestCase
from catalog.models import Item, Category
from django.http import QueryDict
from django_dynamic_fixture import get
from utils.strings import translit
from orders.models import OrderItem, Order, NEW
from django.contrib.auth.models import User
from pages.models import Page, RedirectPage
from xml.dom import minidom
from django.core.urlresolvers import reverse
import time
from utils.policy import javascript_block

class PageParserTest(TestCase):
    fixtures = ['categories.json']
    def setUp(self):
        self.user = User.objects.create_superuser('chapson', 'mrdark@list.ru', '1')
        self.user1 = User.objects.create_superuser('zver', 'anton@list.ru', '1')
        self.client.login(username='chapson', password='1')
        title = u"destination page!"
        post = {'body': BODY, 'title': 'old url'}
        self.client.post('/administration/pages/add/', post)
        post = {'body': BODY, 'title': title}
        page = Page.objects.all()[0]
        self.client.post('/administration/pages/%d/edit/' % page.id, post)
            
        self.item = get(Item, name = "A cosmic ship", 
                        description = "some cosmic ship",
                        url = "a-cosmic-ship")
        title = u"page with links"
        post = {'body': BODY_LINKED, 
                'title': title,
                }
        self.client.post('/administration/pages/add/', post)
        self.page = Page.objects.all()[1]
        self.before_page = Page.objects.all()[0]
        self.dom = minidom.parseString('<root>%s</root>' % self.page.formatted_body.encode('UTF-8'))
                
    def test_links_to_page(self):
        links = self.dom.getElementsByTagName('a')
        self.failUnlessEqual(len(links), 11, "Must be 9 links")
        
        url = reverse('show_page', kwargs={'url': self.before_page.url})
        self.failUnlessEqual(links[0].attributes['href'].value, url, "Must point to page")
        self.failUnlessEqual(links[1].attributes['href'].value, url, "Must point to page")
        self.failUnlessEqual(links[2].attributes['href'].value, url, "Must point to page")
        self.failUnlessEqual(links[3].attributes['href'].value, url, "Must point to page")
        self.failUnlessEqual(links[4].attributes['href'].value, url, "Must point to page")
        self.failUnlessEqual(links[5].attributes['href'].value, url, "Must point to page")
        self.failUnlessEqual(links[6].attributes['href'].value, url, "Must point to redirect page")
        
        url = reverse('show_item', kwargs={'url': self.item.url})
        self.failUnlessEqual(links[7].attributes['href'].value, url, "Must point to Item")
        self.failUnlessEqual(links[8].attributes['href'].value, url, "Must point to Item")
        self.failUnlessEqual(links[9].attributes['href'].value, url, "Must point to Item")
        
        self.failUnlessEqual(links[9].attributes['class'].value, javascript_block('pagelink'), "Must be marked as item link")
        self.failUnlessEqual(links[10].attributes['class'].value, javascript_block('externallink'), "Must be marked as external link")
        
    def test_headers(self):
        heads = self.dom.getElementsByTagName('h2')
        self.failUnlessEqual(len(heads), 5, "Must have 5 H2's")
        self.failUnlessEqual(unicode(heads[0].childNodes[0].nodeValue), u'страница со ссылками', "Head must be exact with no spaces etc")
        
BODY = u"""
=== заголовок ===
[[new page]]

какой то текст!
еще
немного

==== заголовок 2 ====
все
"""

BODY_LINKED = u"""
= страница со ссылками =

== ссылки на страницы ==
ссылка по url: [[destination-page]]
ссылка по url со слешами [[/destination-page]] [[destination-page/]] [[/destination-page/]]
ссылка по заголовку [[destination page!]]
piped link: [[destination page!|текст ссылки]]

== redirect links ==
[[old-url|Link to old URL]]

== ссылки на товары ==
ссылка на товар по url [[a-cosmic-ship]]
ссылка на товар по имени [[A cosmic ship]]
piped link [[a-cosmic-ship|Хороший товар!!]]


== внешняя ссылка ==
http://www.mediawiki.org/wiki/MediaWiki


"""
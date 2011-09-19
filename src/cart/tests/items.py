# -*- coding:utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from catalog.models import Item
from django.core.urlresolvers import reverse
from django.utils import simplejson

class CartItemsTest(TestCase):
    fixtures = ['categories.json']
    def setUp(self):
        self.user = User.objects.create_superuser('zver', 'anton@list.ru', '1')
        self.client.login(username='zver', password='1')
    
    def test_quantity(self):
        item = Item.public_objects.all()[0]
        post = {'quantity': 2}
        headers = {'HTTP_X_REQUESTED_WITH': True}
        self.failIf('cart' in self.client.session, "Must be no cart yet")
        result = self.client.post(reverse('cart_item_quantity', kwargs={'url': item.url}),
                                  post,
                                  **headers)
        self.failUnlessEqual(result.status_code, 200, "A correct request")
        data = simplejson.loads(result.content)
        self.failUnless('cart' in data, "Must have 'cart' in data")
        self.failUnless('price' in data, "Must have 'price' in data")
        self.failUnless('total_price' in data, "Must have 'total_price' in data")
        
        cart_items = data['cart']['items']
        self.failUnlessEqual(len(cart_items), 1, "Must be 1 item in cart")
        keys_in_data = ('url', 'quantity', 'price', 'added_at')
        for key in keys_in_data:
            self.failUnless(key in cart_items[0], "This key (%s) must be in response json")
        self.failUnlessEqual(item.url, cart_items[0]['url'], "URL must be the same")
        
        self.failUnless('cart' in self.client.session, "Cart must be enabled")
        cart = self.client.session['cart']
        self.failUnless('items' in cart, "Must have items in cart")
        items = cart['items']
        self.failUnlessEqual(len(items), 1, "Must have 1 item in cart")
        self.failUnlessEqual(items[0]['url'], item.url, "URL be the same")
        self.failUnless('added_at' in items[0], "Must have added_at in items")
        
        item2 = Item.public_objects.all()[1]
        post = {'quantity': 4}
        result = self.client.post(reverse('cart_item_quantity', kwargs={'url': item2.url}),
                                  post,
                                  **headers)
        self.failUnlessEqual(result.status_code, 200, "A correct request")
        cart = self.client.session['cart']
        self.failUnless('items' in cart, "Must have items in cart")
        items = cart['items']
        self.failUnlessEqual(len(items), 2, "Must have 2 items in cart")
        self.failUnlessEqual(items[0]['url'], item.url, "Must have url in items")
        self.failUnlessEqual(items[1]['url'], item2.url, "Must have url in items")
        
        post = {'quantity': 0}
        result = self.client.post(reverse('cart_item_quantity', kwargs={'url': item2.url}),
                                  post)
        self.failUnlessEqual(result.status_code, 302, "A correct request")
        cart = self.client.session['cart']
        self.failUnless('items' in cart, "Must have items in cart")
        items = cart['items']
        self.failUnlessEqual(len(items), 1, "Must have removed 1 item")
        self.failUnlessEqual(items[0]['url'], item.url, "Must have left only first item")
        
    def test_relative_quantity(self):
        item = Item.public_objects.all()[0]
        headers = {'HTTP_X_REQUESTED_WITH': True}
        post = {'quantity': "+1"}
        self.client.post(reverse('cart_item_quantity', kwargs={'url': item.url}),
                         post,
                         **headers)
        post = {'quantity': "+2"}
        result = self.client.post(reverse('cart_item_quantity', kwargs={'url': item.url}),
                                  post,
                                  **headers)
        self.failUnlessEqual(result.status_code, 200, "A correct request")
        
        self.failUnless('cart' in self.client.session, "Cart must be enabled")
        cart = self.client.session['cart']
        items = cart['items']
        self.failUnlessEqual(len(items), 1, "Must have 1 item in cart")
        self.failUnlessEqual(3, items[0]['quantity'], "Must have 3 items")
        
        post = {'quantity': "-1"}
        result = self.client.post(reverse('cart_item_quantity', kwargs={'url': item.url}),
                                  post,
                                  **headers)
        cart = self.client.session['cart']
        items = cart['items']
        self.failUnlessEqual(2, items[0]['quantity'], "Must have 2 items")

    def test_wrong_request(self):
        item = Item.public_objects.all()[0]
                
        result = self.client.post(reverse('cart_item_quantity', kwargs={'url': item.url}))
        self.failUnlessEqual(result.status_code, 403, "An erroneous request")
        
# -*- coding:utf-8 -*-
from django.utils import simplejson
from utils.base_view import BaseTemplateView
from django.http import HttpResponse, Http404
from catalog.models import Item
import datetime
from django.utils.translation import ugettext
from orders.models import Delivery

def dump_item(item):
    return {'url': item.url,
            'name': item.name,
            'description': item.description,}

class CartQuantityView(BaseTemplateView):
    def post(self, request, url, *args, **kwargs):
#        url = kwargs.pop('url')
        if 'cart' not in self.request.session:
            cart = {'items': [], 'price': 0, 'total_price': 0,
                    }
            self.request.session['cart'] = cart
        else:
            cart = self.request.session['cart']
        try:
            item = Item.public_objects.get(url=url)
        except Item.DoesNotExist:
            return Http404()
        if 'quantity' in self.request.POST:
            action = 0
            if self.request.POST['quantity'].startswith('-'):
                action = -1
            elif self.request.POST['quantity'].startswith('+'):
                action = 1
            quantity = abs(int(self.request.POST['quantity']))
        else:
            return HttpResponse(simplejson.dumps({'item': dump_item(item),
                                                  'message': ugettext('Wrong request')}),
                                mimetype='application/json',
                                status=403)
        cart_item = None
        index = 0
        for some_cart_item in cart['items']:
            if some_cart_item['url'] == url:
                cart_item = some_cart_item
                break
            index += 1
        now = datetime.datetime.now()
        if cart_item is None:
            cart_item = {'url': item.url, 
                         'quantity': 0, 
                         'added_at': now,
                         'price': item.price,
                         }
            cart['items'].append(cart_item)
        if action != 0:
            cart_item['quantity'] = cart_item['quantity'] + action*quantity
            if cart_item['quantity'] < 0:
                cart['items'].pop(index)
        elif quantity == 0:
            cart['items'].pop(index)
        else:
            cart_item['quantity'] = quantity
           
        #PRICE
        price = 0
        for item in cart['items']:
            price += item['price']*item['quantity']
        
        request.session.save()
        content = {'cart': {'items': []},
                   'price': price,
                   'total_price': price}
        for item in cart['items']:
            content['cart']['items'].append({'url': item['url'],
                                             'quantity': item['quantity'],
                                             'added_at': item['added_at'].strftime('%m/%d/%Y %H:%M:%S'),
                                             'price': item['price'],
                                             })
        return HttpResponse(simplejson.dumps(content),
                            mimetype='application/json')
        
class ShowCartView(BaseTemplateView):
    def get(self, *args, **kwargs):
        params = {}
        if 'cart' not in self.request.session:
            cart = {'items': [], 'price': 0, 'total_price': 0,
                    }
            self.request.session['cart'] = cart
        else:
            cart = self.request.session['cart']
        delivery_types = Delivery.public_objects.all()
        params['delivery_types'] = delivery_types
        
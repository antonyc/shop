# -*- coding:utf-8 -*-
from _collections import defaultdict
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.utils.decorators import method_decorator
from itertools import ifilter
import math
from administration.deliveries.views import AddressForm
from business_events.models import Event
from loginza.decorators import login_required
from utils.base_view import BaseTemplateView, set_cart, get_address_text
from django.http import HttpResponse, Http404, HttpResponseRedirect
from catalog.models import Item
import datetime
from django.utils.translation import ugettext
from orders.models import Delivery, Order, OrderItem, OrderStatuses

def dump_item(item):
    return {'url': item.url,
            'name': item.name,
            'description': item.description,}

class CartQuantityView(BaseTemplateView):
    def post(self, request, url, *args, **kwargs):
        cart = set_cart(self.request.session)
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
                         'id': item.id,
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

        cart['price'] = cart['total_price'] = round(price, 2)
        
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
        if self.request.is_ajax:
            content = content.copy()
            content['message'] = ugettext('Item added successfully')
            content['show_quantity'] = cart_item['quantity']
            return HttpResponse(simplejson.dumps(content),
                                mimetype='application/json')
        else:
            return self.redirect_to_referrer()

class ShowCartView(BaseTemplateView):
    template_name = 'cart/show.html'
    count_visits = True
    def prepare_cart_params(self):
        cart = set_cart(self.request.session)
        items = []
        for item in cart.get('items',[]):
            try:
                item = {'obj': Item.public_objects.get(url=item['url']),
                        'quantity': item['quantity'],}
                items.append(item)
            except Item.DoesNotExist:
                pass
        self.params['items'] = items
        deliveries = Delivery.public_objects.all()
        template_dt = defaultdict(list)
        self.params['delivery_types'] = template_dt
        self.params['delivery_chosen'] = int(cart['delivery'].get('id', 0))
        for delivery in deliveries:
            template_dt[delivery.type].append(delivery)
        self.params['address_form'] = AddressForm(prefix="address", initial=cart['address'])

    def get(self, *args, **kwargs):
        self.prepare_cart_params()
        return self.render_to_response(self.params)

    def post(self, *args, **kwargs):
        def validate_request():
            errors = defaultdict(list)
            keys = post.keys()
            has_items = False
            items_ok = True
            for item_id in ifilter(lambda _: _.startswith('cart_item_id_'), keys):
                has_items = True
                try:
                    item_id = int(item_id[len('cart_item_id_'):])
                except ValueError:
                    items_ok = False
                    errors['item'].append(ugettext("'%s' is not a valid integer"))
                    break
                try:
                    order_items.append(Item.public_objects.get(id=item_id))
                except Item.DoesNotExist:
                    items_ok = False
                    errors['item'].append(ugettext("Item with such id does not exist '%s'") % item_id)
                    break
            if not has_items:
                errors['item'].append(ugettext("You should go back to the store and pick up some goods"))
            delivery_id = post.get('delivery_id')
            if delivery_id is None:
                errors['delivery'].append(ugettext("You must choose one delivery"))
            else:
                try:
                    delivery = Delivery.public_objects.get(id=delivery_id)
                except Delivery.DoesNotExist:
                    errors['delivery'].append(ugettext("No such delivery '%s'") % delivery_id)
            return errors
        order_items = []
        post = self.request.POST
        cart = set_cart(self.request.session, post)
        errors = validate_request()
        try:
            delivery = Delivery.public_objects.get(id=cart['delivery'].get('id'))
        except Delivery.DoesNotExist:
            if not errors.get('delivery'):
                errors['delivery'].append(ugettext("Such delivery does not exist"))
        if errors:
            self.params['errors'] = errors
            self.prepare_cart_params()
            if self.request.is_ajax:
                return HttpResponse(simplejson.dumps(errors), mimetype='application/json')
            return self.render_to_response(self.params)
        order = Order(delivery=delivery, user=self.request.user)
        order.save()
        for item in order_items:
            order_item = OrderItem(item=item, quantity=post['cart_item_id_'+str(item.id)], price=item.price)
            order.orderitem_set.add(order_item)
        order.save()
        for key in cart['address']:
            order.dynamic_properties['address'] = {'text': cart['address']}
        order.dynamic_properties.save()
        event = Event(user=self.request.user)
        event.save()
        event.dynamic_properties['event'] = {'order_id': order.id,
                                             'type': 'order_created'}
        event.save()
        del self.request.session['cart']
        url = reverse('view_order', kwargs={'id': order.id})
        if self.request.is_ajax:
            return HttpResponse(simplejson.dumps({'url': url}),
                                mimetype='application/json')
        return HttpResponseRedirect(url)
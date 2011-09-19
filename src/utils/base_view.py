# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

class BaseTemplateView(TemplateView):
    def dispatch(self, *args, **kwargs):
        self.params = {}
        self.request = args[0]
        if self.request.META.get('HTTP_X_REQUESTED_WITH'):
            self.request.is_ajax = True
        else:
            self.request.is_ajax = False
        return super(BaseTemplateView, self).dispatch(*args, **kwargs)
    
    def render_to_response(self, context, **response_kwargs):
        if context is not None:
            context['request'] = self.request
            cart = set_cart(self.request.session)
            context['simple_cart_total_price'] = cart['total_price']

        return super(BaseTemplateView, self).render_to_response(context, **response_kwargs)

    def redirect_to_referrer(self):
        referrer = self.request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(referrer)

def get_address_text(post):
    result = {}
    fields = ['country', 'city', 'street', 'city__text', 'country__text', 'building', 'office', 'description']
    for field in fields:
        value = post.get('address-'+field)
        if value is not None:
            if field in ('country', 'city'):
                try:
                    value = int(value)
                except ValueError:
                    pass
            result[field] = value
    if not result.get('city__text') and result.get('city'):
        result['city'] = ''
    if not result.get('country__text') and result.get('country'):
        result['country'] = ''
    return result

def set_cart(session, post=None):
    default_cart = {'items': [],
                    'delivery': {},
                    'price': 0,
                    'total_price': 0,
                    'address': {}}
    if 'cart' not in session:
        session['cart'] = default_cart.copy()
    else:
        for key in default_cart:
            if key not in session['cart']:
                if hasattr(default_cart[key], 'copy'):
                    session['cart'][key] = default_cart[key].copy()
                else:
                    session['cart'][key] = default_cart[key]
    cart = session['cart']
    if post is not None:
        for item in cart['items']:
            quantity = post.get('cart_item_id_'+str(item['id']))
            if quantity:
                item['quantity'] = quantity
        delivery_id = post.get('delivery_id')
        if delivery_id:
            cart['delivery']['id'] = delivery_id
        addr = get_address_text(post)
        if addr:
            cart['address'] = addr
        else:
            cart['address'] = {}
    return session['cart']
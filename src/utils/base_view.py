# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.utils.translation import ngettext
from django.views.generic.base import TemplateView
from utils import site_settings
from utils.menu import build_menu, parse_menu
from orders.models import Order

class BaseTemplateView(TemplateView):
    count_visits = False
    def dispatch(self, *args, **kwargs):
        self.params = {}
        self.request = args[0]
        if self.request.META.get('HTTP_X_REQUESTED_WITH'):
            self.request.is_ajax = True
        else:
            self.request.is_ajax = False
        return super(BaseTemplateView, self).dispatch(*args, **kwargs)

    def page_visits_counter(self):
        return """<!-- Yandex.Metrika counter --><div style="display:none;"><script type="text/javascript">(function(w, c) { (w[c] = w[c] || []).push(function() { try { w.yaCounter9938191 = new Ya.Metrika({id:9938191, enableAll: true}); } catch(e) { } }); })(window, "yandex_metrika_callbacks");</script></div><script src="//mc.yandex.ru/metrika/watch.js" type="text/javascript" defer="defer"></script><noscript><div><img src="//mc.yandex.ru/watch/9938191" style="position:absolute; left:-9999px;" alt="" /></div></noscript><!-- /Yandex.Metrika counter -->"""

    def render_to_response(self, context, **response_kwargs):
        if context is not None:
            context['request'] = self.request
            cart = set_cart(self.request.session)
            context['cart'] = cart
            context['simple_cart_total_price'] = cart['total_price']
            count_items = reduce(lambda a, b: a + int(b['quantity']), cart['items'], 0)
            context['simple_cart_item_count_items'] = ngettext("item", "items", count_items)
            if self.count_visits:
                context['count_visits'] = self.page_visits_counter()
            context['simple_cart_item_quantity'] = count_items
            menu = site_settings['top_menu'] or {}
            context['top_menu'] = build_menu(menu.get('parsed', {}))
            if self.request.user.is_authenticated:
                statuses = (Order.ORDER_STATUSES.new, Order.ORDER_STATUSES.processed)
                if self.request.user.is_authenticated():
                    orders = Order.objects.filter(user=self.request.user, status__in=statuses).order_by('-created_at')[0:1]
                else:
                    orders = []
                if orders:
                    context['latest_order'] = orders[0]

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
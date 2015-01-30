# -*- coding: utf-8 -*-
__author__ = 'chapson'

from django.utils import translation
from django.utils.translation import ugettext
from geocoding.models import Geomodel
from utils import policy
from orders.models import get_address, STATUSES
from utils.templatetags.util_tags import class_block
from administration.deliveries.views import AddressForm
from django import template
register = template.Library()


@register.simple_tag
def print_delivery_address(delivery):
    text = ''
    has_text_address = delivery.dynamic_properties.has_text_address()
    if has_text_address:
        addr = get_address(delivery.dynamic_properties)
        if 'country__text' in addr:
            addr['country'] = addr['country__text']
        if 'city__text' in addr:
            addr['city'] = addr['city__text']
        commaseparated_groups = (('country',), ('city',), ('street','building',), ('office',))
        address = []
        for group in commaseparated_groups:
            result = []
            for element in group:
                if addr.get(element):
                    result.append("<span class=\"%(klass)s\">%(text)s</span>" % {'klass': element,
                                                                                 'text': addr.get(element, '')})
            if result:
                address.append(" ".join(result))
        text += ", ".join(address) + "."
        if 'description' in addr:
            text += " " + addr["description"].strip(".").strip() + "."
    return text

@register.simple_tag
def delivery_address(delivery, editable=False):
    text = ''
    editable = int(bool(editable))
    has_text_address = delivery.dynamic_properties.has_text_address()
    if has_text_address or editable:
        result = []
        if has_text_address:
            addr = get_address(delivery.dynamic_properties)
        else:
            addr = {}
        initial = {}
        for element in ('country', 'country__text', 'city__text', 'city', 'street', 'building', 'office', 'description'):
            if addr.get(element, None):
                initial[element] = addr[element]
            else:
                initial[element] = ''
        form = AddressForm(initial=initial, prefix="address")
        
        text += "<div class=\"%(klass)s\" onclick=\"return {}\"><ul>%(form)s</ul></div>" % {'form': form.as_ul(),
                                                                      'klass': class_block('delivery_address')}
    return text
@register.simple_tag
def delivery_map(delivery, editable=False, map_visible=False, text=None):
    text = ''
    editable = int(bool(editable))
    map_visible = bool(map_visible)
#    show_link = int(bool(show_link))
    klass = class_block('delivery_map__text')
    if delivery.dynamic_properties.has_point() or editable:
        klass += ' ' + class_block('mocklink')
    map = ''
    has_point = delivery.dynamic_properties.has_point()
    if has_point or editable:
        if not text:
            if editable:
                text = ugettext("hide or show")
            else:
                text = ugettext('Show on the map')
        text = """<span class="%(blockname)s">%(address)s</span>""" % {'address': text,
                                                                       'blockname': klass}
        map = """<div class="%(blockname)s"><div></div></div>""" % {'blockname': class_block('delivery_map__map')}
    return "<div onclick=\"return {map_visible: %(map_visible)s, lat: %(lat)s, lon: %(lon)s, editable: %(editable)s}\" class=\"%(class)s\">%(text)s</div>" % {
        'class': class_block('delivery_map'),
        'text': text + map,
        'map_visible': str(map_visible).lower(),
        'lat': delivery.dynamic_properties['address']['point']['lat'] if has_point else 'undefined',
        'lon': delivery.dynamic_properties['address']['point']['lon'] if has_point else 'undefined',
        'editable': editable}

@register.filter
def order_status(order):
    return dict(STATUSES).get(order.status, ugettext('unknown'))

@register.simple_tag
def decorate_currency(price):
    number = "%.2f" % price
    return "<span class=\"integer\">%s</span><span class=\"remainder\">%s</span>" % (number[:-3], number[-2:])

@register.simple_tag
def orderitem_price(orderitem):
    return decorate_currency(orderitem.price*orderitem.quantity)
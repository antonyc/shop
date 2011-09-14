# -*- coding: utf-8 -*-
from django.utils import translation
from django.utils.translation import ugettext
from geocoding.models import Geomodel
from utils import policy
from orders.models import get_address
from utils.templatetags.util_tags import class_block
from administration.deliveries.views import AddressForm
from django import template
register = template.Library()

__author__ = 'chapson'

@register.simple_tag
def delivery_address(delivery, editable=False):
    text = ''
    editable = int(bool(editable))
#    print delivery.dynamic_properties.has_text_address()
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
def delivery_map(delivery, editable=False, map_visible=False, show_link=True):
    text = ''
    editable = int(bool(editable))
    map_visible = bool(map_visible)
#    show_link = int(bool(show_link))
    klass = class_block('delivery_map__text')
    if delivery.dynamic_properties.has_point() or editable:
        klass += ' ' + class_block('mocklink')
    if editable:
        text = ugettext("Edit")
    else:
        text = ugettext('Show on the map')
    text = """<span class="%(blockname)s">%(address)s</span>""" % {'address': text,
                                                                   'blockname': klass}
    map = ''
    has_point = delivery.dynamic_properties.has_point()
    if has_point or editable:
        map = """<div class="%(blockname)s" onclick="return {lat: %(lat)s, lon: %(lon)s, editable: %(editable)s}"><div style="height: 400px;"></div></div>"""
        map = map % {'blockname': class_block('delivery_map__map'),
                     'lat': delivery.dynamic_properties['address']['point']['lat'] if has_point else 'undefined',
                     'lon': delivery.dynamic_properties['address']['point']['lon'] if has_point else 'undefined',
                     'editable': editable}
    return "<div onclick=\"return {map_visible: %(map_visible)s}\" class=\"%(class)s\">%(text)s</div>" % {'class': class_block('delivery_map'),
                                                                                                          'text': text + map,
                                                                                                          'map_visible': str(map_visible).lower()}
# -*- coding: utf-8 -*-
from django.utils import translation
from django.utils.translation import ugettext
from geocoding.models import Geomodel
from utils import policy
from orders.models import get_address
from utils.templatetags.util_tags import class_block
from django import template
register = template.Library()

__author__ = 'chapson'

@register.simple_tag
def delivery_text_address(delivery, editable=False, map_visible=False, show_address=True):
    text = ''
    editable = int(bool(editable))
    map_visible = bool(map_visible)
    show_address = int(bool(show_address))
    if delivery.dynamic_properties.has_address and show_address:
        addr = get_address(delivery.dynamic_properties)
        address = []
        for element in ('country', 'city', 'street', 'building', 'office'):
            if addr.get(element,None): address.append(addr[element])
        description = addr.get('description', '')
        klass = class_block('delivery_map__text')
        if delivery.dynamic_properties['address'].get('point') or editable:
            klass += ' ' + class_block('mocklink')
        text = """<span class="%(blockname)s">%(address)s</span> %(description)s""" % {'address': ', '.join(address),
                                                                                       'blockname': klass,
                                                                                       'description': description}

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
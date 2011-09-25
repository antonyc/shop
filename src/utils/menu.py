# -*- coding: utf-8 -*-
from xml.dom import minidom
from utils.strings import parse_markup

__author__ = 'chapson'


def parse_menu(text):
    menu = {'text': text,
            'parsed': []}
    text = text.replace("\r\n", "\n").strip()
    parsed_text = parse_markup(text, 'parsed')
    tree = minidom.parseString(parsed_text.encode('UTF-8'))
    for node in tree.childNodes[0].childNodes:
        if getattr(node, 'tagName', None) == 'a':
            for anchor_child in node.childNodes:
                if isinstance(anchor_child, minidom.Text):
                    attrs = dict(map(lambda attr: (attr.nodeName, attr.value),
                                     node._attrs.itervalues()))
                    anchor = {'text': anchor_child.data,
                              'attrs': attrs}
                    menu['parsed'].append(anchor)
    return menu


def build_menu(menu):
    result = []
    for element in menu:
        attrs = map(lambda e: "%s=\"%s\"" % e,
                    element['attrs'].iteritems())
        result.append("<a %s>%s</a>" % (" ".join(attrs), element['text']))
    return result
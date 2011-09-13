# -*- coding: utf-8 -*-

from utils import policy
from django.db import models
from string import maketrans
from mwlib.uparser import parseString
from mwlib.parser.nodes import ArticleLink
from mwlib.xhtmlwriter import MWXHTMLWriter as Writer
#from pages.models import Page
from catalog.models import Item
from django.core.urlresolvers import reverse
try:
    import xml.etree.ElementTree as ET
except:
    from elementtree import ElementTree as ET
from BeautifulSoup import BeautifulStoneSoup
from django.utils.log import NullHandler
from mwlib.xhtmlwriter import log
log = NullHandler()
from mwlib.dummydb import DummyDB
import StringIO
from django.utils.encoding import smart_unicode
import trans
import re
    
input = u"""
=h1=

*item 1
*item2

A few lines of 
text in this article.

И  еще пара строк
==h2==

some [[Link|caption]] there
"""

class MyWriter(Writer):
    header = ""
    css = None
    paratag = 'div'
    
    def __init__(self, **kwargs):
        Writer.__init__(self, **kwargs)
        self.root = self.xmlbody = ET.Element("div")
    
    def xwriteLink(self, obj): # FIXME (known|unknown)
        obj.url = parse_interwiki_link(obj.target)
        a = ET.Element("a", href=obj.url or "#")
        for attr, value in obj.attributes:
            a.set(attr, value)
        klass = obj.vlist.get('class', policy.javascript_block('pagelink')) 
        a.set("class", klass)
        if not obj.children:
            a.text = obj.target
        return a
    
    def xwriteStyle(self, obj):
        tag = 'span'
        if obj.caption == "''":
            tag = 'em'
        elif obj.caption == "'''":
            tag = 'strong'
        el = ET.Element(tag)
        return el
    
    xwriteArticleLink = xwriteLink
    
    def xwriteURL(self, obj):
        a = ET.Element("a", href=obj.caption)
        a.set("class", policy.javascript_block('externallink'))
        if not obj.children:
            a.text = obj.caption
        return a
    
    def xwriteSection(self, obj):
        tree = super(MyWriter, self).xwriteSection(obj)
        tree.set('class', policy.javascript_block('section'))
        tree[0].text = tree[0].text.strip()
        return tree

def parse_markup(body, title='Some article'):
    db = DummyDB()
    if body.endswith(chr(13)+chr(10)):
        body = body.replace(chr(13)+chr(10),chr(10))
    p = parseString(title, body, db)
    result = MyWriter().write(p)
    result = ET.tostring(result)
    return unicode(BeautifulStoneSoup(result, convertEntities=BeautifulStoneSoup.HTML_ENTITIES))

replacement_regexp = re.compile(r'(\W+)', re.IGNORECASE)

def translit(s):
    """
    Accepts only unicode, works on pypi "trans" module
    """
    return re.sub(replacement_regexp, '-', s.encode('trans').strip('-')).strip('-')

def get_page(target):
    from pages.models import Page, RedirectPage
    try:
        return Page.objects.get(url=target)
    except Page.DoesNotExist:
        pass
    try:
        return Page.objects.get(title=target)
    except Page.DoesNotExist:
        pass
    try:
        redirect = RedirectPage.objects.select_related('to_page').get(from_url=target)
        return redirect.to_page
    except RedirectPage.DoesNotExist:
        pass

def get_item(target):
    from catalog.models import Item
    try:
        return Item.public_objects.get(models.Q(url=target)|models.Q(name=target))
    except Item.DoesNotExist:
        pass
    
def parse_interwiki_link(target):
    page = get_page(target.strip('/'))
    if page is not None:
        return reverse('show_page', kwargs={'url': page.url})
    item = get_item(target.strip('/'))
    if item is not None:
        return reverse('show_item', kwargs={'url': item.url})
    return target
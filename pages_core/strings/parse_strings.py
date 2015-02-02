# -*- coding: utf-8 -*-
import re

from mwlib.uparser import parseString
from django.core.urlresolvers import reverse
from BeautifulSoup import BeautifulStoneSoup
from mwlib.dummydb import DummyDB
from xml.dom import minidom
import xml.etree.ElementTree as ET

from policy import javascript_block
from .writer import MWXHTMLWriter as Writer


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
    
    def xwriteLink(self, obj):  # FIXME (known|unknown)
        obj.url = parse_interwiki_link(obj.target)
        a = ET.Element("a", href=obj.url or "#")
        for attr, value in obj.attributes:
            a.set(attr, value)
        klass = obj.vlist.get('class', javascript_block('pagelink'))
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
        a.set("class", javascript_block('externallink'))
        if not obj.children:
            a.text = obj.caption
        return a
    
    def xwriteSection(self, obj):
        tree = super(MyWriter, self).xwriteSection(obj)
        tree.set('class', javascript_block('section'))
        tree[0].text = tree[0].text.strip()
        return tree

images_reg = re.compile("<<images\s*([\d,? ?]+)\s*>>")
images_container = "<div class=\"" + javascript_block('page_container_images') + "\">%s</div>"""
image_template = """<div class="%(blockname)s">
<ul class="thumbs noscript">%(images)s</ul>
</div>
<div class="block-page_images__clear_fix"></div>
"""
image_block_template = """<li>
<a class="thumb %(image_block)s" href="%(href)s">
<img src="%(imagesrc)s" alt="%(imagealt)s" /></a>
</li>
"""

"""
def make_images(body):
    def replacer(match):
        ids = match.groups()[0].split(",")
        image_ids = map(lambda x: x.strip(), ids)
        from pages.models import PageImage
        images = PageImage.objects.filter(id__in=image_ids)
        if len(images) == 1:
            i = images[0]
            return images_container % ("<img src=\"" + \
                   gen_thumbnail(i.image, settings.THUMBNAILS['large']) + \
                   "\" alt=\"" + i.alt + "\" />")
        image_html = "\n".join(map(lambda i: image_block_template % {
            'image_block': javascript_block('page_images__image'),
            'href': gen_thumbnail(i.image, settings.THUMBNAILS['large']),
            'imagesrc': gen_thumbnail(i.image, settings.THUMBNAILS['bigger']),
            'imagealt': i.alt,
        }, images))
        result = images_container % ''
        result += image_template % {'blockname': javascript_block('page_images'),
                                 'images': image_html,
                                 }
        return result
    return re.sub(images_reg, replacer, body)
"""


def parse_markup(body, title='Some article', strip_title=True, **kwargs):
    db = DummyDB()
    if body.endswith(chr(13)+chr(10)):
        body = body.replace(chr(13)+chr(10), chr(10))
    p = parseString(title, body, db)
    result = MyWriter().write(p)
#    if strip_title and result._children[0].tag == 'h1':
#        result._children = result._children[1:]
    result = ET.tostring(result)
    if strip_title:
        parse = minidom.parseString(result)
        h1 = parse.childNodes[0].childNodes[0]
        if h1.tagName == 'h1':
            parse.childNodes[0].removeChild(h1)
            res = parse.toxml()
            result = res[res.find('?>')+2:]
    body = unicode(BeautifulStoneSoup(result, convertEntities=BeautifulStoneSoup.HTML_ENTITIES))
    #body = make_images(body)  no images for now
    return body

replacement_regexp = re.compile(r'(\W+)', re.IGNORECASE)


def translit(s):
    """
    Accepts only unicode, works on pypi "trans" module
    """
    # init trans module
    import trans  # no-qa
    return re.sub(replacement_regexp, '-', s.encode('trans').strip('-')).strip('-')


def get_page(target):
    from pages_core.logic import (
        get_page_by_title, get_page_by_url,
    )
    page = get_page_by_url(target)
    if page:
        return page
    page = get_page_by_title(target)
    if page:
        return page
    return None


def parse_interwiki_link(target):
    page = get_page(target.strip('/'))
    if page is not None:
        return reverse('show_page', kwargs={'url': page.url})
    return target

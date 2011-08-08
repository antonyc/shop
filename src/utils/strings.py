# -*- coding: utf-8 -*-

from string import maketrans
from mwlib.uparser import parseString
from mwlib.xhtmlwriter import MWXHTMLWriter as Writer
try:
    import xml.etree.ElementTree as ET
except:
    from elementtree import ElementTree as ET
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
    def __init__(self, **kwargs):
        Writer.__init__(self, **kwargs)
        self.root = self.xmlbody = ET.Element("div")

writer = MyWriter()

def parse_markup(body):
    db = DummyDB()
    if body.endswith(chr(13)+chr(10)):
        body = body.replace(chr(13)+chr(10),chr(10))
    p = parseString('Some article', body, db)
    result = writer.write(p)
    return ET.tostring(result)

replacement_regexp = re.compile(r'(\W+)', re.IGNORECASE)

def translit(s):
    """
    Accepts only unicode, works on pypi "trans" module
    """
    return re.sub(replacement_regexp, '-', s.encode('trans'))

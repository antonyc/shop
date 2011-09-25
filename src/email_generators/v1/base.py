__author__ = 'chapson'
from django.conf import settings
from base64 import encodestring


class BaseGenerator(object):
    def trash(self):
        return []

    def events_by_type(self, events, _type):
        result = []
        for e in events:
            print e.dynamic_properties.fetchDocument()
            if e.dynamic_properties.fetchDocument().get('event', {}).get('type', None) ==  _type:
                result.append(e)
        print result
        return result

    def email_name(self, name, email):
        name = encodestring(unicode(name).encode('UTF-8'))[:-1].replace("\n", '')
        return '=?utf-8?B?%s?= <%s>' % (name, email),
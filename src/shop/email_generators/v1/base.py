from utils import email_name

__author__ = 'chapson'
from django.conf import settings


class BaseGenerator(object):
    def trash(self):
        return []

    def events_by_type(self, events, _type):
        """  filter list of events be given type """
        result = []
        for e in events:
            print e.dynamic_properties.fetchDocument()
            if e.dynamic_properties.fetchDocument().get('event', {}).get('type', None) ==  _type:
                result.append(e)
        return result

    def email_name(self, name, email):
        return email_name(name, email)
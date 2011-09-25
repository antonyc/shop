
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from pymongo import Connection, errors

def is_staff(u):
    return u.is_staff or u.is_superuser

if not hasattr(settings, 'MONGO_DATABASES'):
    raise ImproperlyConfigured('Use MONGO_DATABASES in settings')

mongo_settings = settings.MONGO_DATABASES['default']
mongo_connection = Connection(host=mongo_settings['HOST'])
mongo_db = getattr(mongo_connection, mongo_settings['NAME'])


class MongoPatch(object):
    def __init__(self, handler_class, collection_name):
        assert handler_class is not None
        assert isinstance(collection_name, basestring)
        self.handler_class = handler_class
        self.collection_name = collection_name
        self.signature = '__%s_%s_%s' % (str(self.__class__), str(handler_class), collection_name)

    def __get__(self, obj, type=None):
        if not hasattr(obj, self.signature):
            collection = getattr(mongo_db, self.collection_name)
            setattr(obj, self.signature, self.handler_class(obj, collection))
        return getattr(obj, self.signature)

    def __set__(self, obj, value):
        pass

    def __delete__(self, obj):
        pass

class MongoManager(object):
    default_document = {'api': {'version': '1'}}
    def __init__(self, obj, collection):
        self.obj = obj
        self.collection = collection

    def fetchDocument(self):
        self.document = self.collection.find_one(self.obj.pk)
        if self.document is None:
            document = self.default_document.copy()
            document['_id'] = self.obj.pk
            self.collection.insert(document)
            self.document = document
        return self.document
#        return self.document

    def __getitem__(self, item):
        return self.fetchDocument()[item]

    def __setitem__(self, key, value):
        self.fetchDocument()[key] = value
        self.collection.update({'_id': self.obj.pk}, {"$set": {key: value}}, upsert=True)

    def __delitem__(self, key):
        doc = self.fetchDocument()
        del doc[key]
        self.save()

    def __contains__(self, item):
        return item in self.fetchDocument()

    def __str__(self):
        return repr(self.fetchDocument())

    def save(self):
        doc = self.fetchDocument()
        doc['_id'] = self.obj.pk
        self.collection.remove(self.obj.pk)
        self.collection.insert(doc)

    def removeDocument(self):
        self.collection.remove(self.obj.pk)


class SiteSettings(object):
    collection_name = 'site_settings'
    _collection = None

    @property
    def collection(self):
        if self._collection is None:
            self._collection = getattr(mongo_db, self.collection_name)
        return self._collection

    def __getitem__(self, item):
        document = self.collection.find_one(item) or {}
        return document.get('value', None)

    def __setitem__(self, key, value):
        self.collection.update({'_id': key}, {"$set": {'value': value}}, upsert=True)

    def __unicode__(self):
        return unicode(list(self.collection.find())[:20])

site_settings = SiteSettings()

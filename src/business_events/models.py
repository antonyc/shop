from collections import defaultdict, namedtuple
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from utils import MongoManager, MongoPatch

class EventPropertiesManager(MongoManager):
    default_document = {'api': {'version': '1'}}
    def api_version(self):
        return self['api']['version']
_event_types = ('time_to_return', 'order_item_change')
EVENT_TYPES = namedtuple('EventType', " ".join(_event_types))._make(_event_types)

class Event(models.Model):
    EVENT_TYPES = EVENT_TYPES
    user = models.ForeignKey(User, null=True, default=None)
    notify = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    dynamic_properties = MongoPatch(EventPropertiesManager, 'business__events')

    def __unicode__(self):
        return "%s at %s (sent? %s)" % (self.user.username if self.user else 'no user',
                                        self.created_at,
                                        self.sent_at)

    @property
    def event_type(self):
        return (self.dynamic_properties.fetchDocument().get('event') or {}).get('type', None)
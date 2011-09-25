from collections import defaultdict, namedtuple
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from utils import MongoManager, MongoPatch

class EventPropertiesManager(MongoManager):
    default_document = {'api': {'version': '1'}}
    def api_version(self):
        return self['api']['version']
    

class Event(models.Model):
    user = models.ForeignKey(User, null=True, default=None)
    notify = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    dynamic_properties = MongoPatch(EventPropertiesManager, 'business__events')

    def __unicode__(self):
        return "%s at %s (sent? %s)" % (self.user.username,
                                        self.created_at,
                                        self.sent_at)
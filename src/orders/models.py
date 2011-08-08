from django.contrib.auth.models import User
from django.db import models
from catalog.models import Item

DELETED = 0
NEW = 2
PROCESSED = 4
DELIVERED = 6
STATUSES = ((DELETED,'deleted'),
            (NEW, 'new'),
            (PROCESSED,'processed'),
            (DELIVERED,'delivered'),)

class OrderManager(models.Manager):
    def get_query_set(self):
        return super(OrderManager, self).get_query_set().filter(status__gt=DELETED)

class Order(models.Model):
    user = models.ForeignKey(User, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUSES, default=NEW)
    
    objects = OrderManager()

class OrderItem(models.Model):
    item = models.ForeignKey(Item, blank=False)
    order = models.ForeignKey(Order, blank=False)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

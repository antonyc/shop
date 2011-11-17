from django.contrib.auth.models import User
from django.utils import translation
from django.db import models
from catalog.models import Item
from django.utils.translation import ugettext, ugettext_lazy
from geocoding.models import Geomodel
from utils import MongoManager, MongoPatch
from collections import namedtuple
from collections import defaultdict
DT_BY_SHOPPER = 'shopper'   
DT_COURIER = 'courier'
DT_MAIL = 'mail'

DS_DELETED = 0
DS_NORMAL = 1

StatusChoices = namedtuple('StatusChoices', 'deleted normal')._make(range(2))
status_choices = ((StatusChoices.deleted, ugettext_lazy('deleted')),
    (StatusChoices.normal, 'normal'))

dt_list = ('shopper', 'courier', 'mail')
DeliveryTypes = namedtuple('DeliveryTypes', ' '.join(dt_list))._make(dt_list)
delivery_types = ((DeliveryTypes.shopper, ugettext_lazy('by shopper himself')),
                  (DeliveryTypes.courier, ugettext_lazy('courier delivery')),
                  (DeliveryTypes.mail, ugettext_lazy('by mail')))


class DeliveryPropertiesManager(MongoManager):
    default_document = defaultdict(dict)
    def has_address(self):
        return 'address' in self

    def has_text_address(self):
        text = self.fetchDocument().get('address',{}).get('text', {})
        return text.get('country', text.get('country__text', False))

    def has_point(self):
        return 'point' in self.fetchDocument().get('address',{})

class DeliveryManager(models.Manager):
    def get_query_set(self):
        return super(DeliveryManager, self).get_query_set().filter(status__gt=0)

class Delivery(models.Model):
    name = models.CharField(max_length=255,blank=False)
    description = models.CharField(blank=False, max_length=255, help_text=ugettext_lazy("Shoppers will see it in their carts"))
    status = models.IntegerField(choices=status_choices, default=StatusChoices.normal)
    type = models.CharField(max_length=20, blank=False, choices=delivery_types)
    price = models.FloatField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    public_objects = DeliveryManager()

    dynamic_properties = MongoPatch(DeliveryPropertiesManager, 'delivery')

    def delete(self, using=None):
        self.dynamic_properties.removeDocument()
        super(Delivery, self).delete()

    def save(self):
        super(Delivery, self).save()
        self.dynamic_properties.save()

    def __unicode__(self):
        return '%d "%s" type "%s"' % (self.pk, self.name, self.type)

def get_address(obj):
    def get_geomodel_in_language(geonameid):
        try:
            geomodel = Geomodel.objects.select_related('geoalternate').get(geonameid=geonameid)
        except Geomodel.DoesNotExist:
            return ugettext('left unresolved') + ' ' + str(geonameid)
        c_qs = geomodel.geoalternate_set.filter(isolanguage=language).order_by('-preferred')
        if c_qs.exists():
            geomodel_name = c_qs.values('variant')[0]['variant']
        else:
            geomodel_name = geomodel.name
        return geomodel_name
    language = translation.get_language()[:2].lower()
    result = {}
    address = obj['address']['text']
    result['country'] = address.get('country', None)
    result['country__text'] = address.get('country__text', None)
    if isinstance(result['country'], int):
        result['country__text'] = get_geomodel_in_language(result['country'])
    result['city__text'] = address.get('city__text', None)
    result['city'] = address.get('city', None)
    if isinstance(result['city'], int):
        result['city__text'] = get_geomodel_in_language(result['city'])
    street = address.get('street', None)
    if street: result['street'] = street
    building = address.get('building', None)
    if building: result['building'] = building
    office = address.get('office', None)
    if office: result['office'] = str(office)
    description = address.get('description', None)
    if description: result['description'] = description
    return result

statuses = "deleted cancelled new processed delivered".split(" ")
DELETED = 0
CANCELLED = 2
NEW = 3
PROCESSED = 6
DELIVERED = 9
statuses_tuple = (DELETED, CANCELLED, NEW, PROCESSED, DELIVERED)
OrderStatuses = namedtuple('OrderStatuses', " ".join(statuses))._make(statuses_tuple)

STATUSES = ((DELETED, ugettext_lazy('deleted')),
            (CANCELLED, ugettext_lazy('cancelled')),
            (NEW, ugettext_lazy('new')),
            (PROCESSED, ugettext_lazy('processed')),
            (DELIVERED, ugettext_lazy('delivered')),)

class OrderManager(models.Manager):
    def get_query_set(self):
        return super(OrderManager, self).get_query_set().filter(status__gt=DELETED)

class OrderPropertiesManager(MongoManager):
    default_document = defaultdict(dict)

    def has_address(self):
        document = self.fetchDocument()
        return 'address' in document

    def has_text_address(self):
        text = self.fetchDocument().get('address',{}).get('text', {})
        return text.get('country', text.get('country__text', False))

class Order(models.Model):
    ORDER_STATUSES = OrderStatuses

    user = models.ForeignKey(User, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUSES, default=NEW)
    delivery = models.ForeignKey(Delivery, blank=False)
    
    objects = models.Manager()
    public_objects = OrderManager()

    dynamic_properties = MongoPatch(OrderPropertiesManager, 'order')

    @property
    def text_status(self):
        return dict(STATUSES).get(self.status, ugettext_lazy('unknown status'))

    def __unicode__(self):
        status = dict(zip(statuses_tuple, statuses)).get(self.status, 'unknown')
        return "%d by \"%s\" status \"%s\"" % (self.id, self.user, status)

    def delete(self, using=None):
        self.dynamic_properties.removeDocument()
        super(Order, self).delete()

    def save(self):
        super(Order, self).save()
        self.dynamic_properties.save()

class OrderItem(models.Model):
    item = models.ForeignKey(Item, blank=False)
    order = models.ForeignKey(Order, blank=False)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(blank=False)

class OrderComment(models.Model):
    order = models.ForeignKey(Order, editable=False)
    user = models.ForeignKey(User, editable=False)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

class Address(models.Model):
    """Model to store addresses for accounts"""
    address_line1 = models.CharField(max_length = 45, help_text=ugettext_lazy("Address Line 1"))
    address_line2 = models.CharField(max_length = 45, help_text=ugettext_lazy("Address Line 1"),
        blank = True)
    postal_code = models.CharField(max_length = 10, help_text=ugettext_lazy("ZIP/Postal code"))
    city = models.CharField(max_length = 50, blank = False)
    state_province = models.CharField(max_length = 40, help_text=ugettext_lazy("State/Province"),
        blank = True)
    country = models.CharField(max_length = 50, blank = True)
    exact_geo_info = models.TextField(blank=True)

    def __unicode__(self):
        return u"%s %s" % (self.city, self.country)
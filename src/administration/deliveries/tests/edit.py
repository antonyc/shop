# -*- coding: utf-8 -*-

from django_dynamic_fixture import get
from django.core.urlresolvers import reverse
from orders.models import Delivery, DeliveryTypes, StatusChoices
from utils.base_testcase import BaseTestCase
from django.contrib.auth.models import User

class DeliveriesEditTestCase(BaseTestCase):
    def setUp(self):
        super(DeliveriesEditTestCase, self).setUp()
        self.setGeoNames()
        self.delivery = get(Delivery, name="Self pick up",
                            description="Pick it up yourself",
                            type=DeliveryTypes.shopper,
                            price=0,
                            status=StatusChoices.normal)
        self.delivery.dynamic_properties['address'] = {'text': {'country': self.russian_federation.geonameid,
                                                                'city': self.irkutsk.geonameid,
                                                                'street': u"Пугачева",
                                                                'building': "4а",
                                                                'office': "5",
                                                                "description": "Say the right name and get it free",
                                                                },
                                                       "point": {'lat': 52.16, 'lon': 104.17}
                                                       }
        self.client.login(username='chapson', password='1')
        
    def test_edit_deliveries(self):
        edit_url = reverse('edit_delivery', kwargs={'id': self.delivery.id})
        result = self.client.get(edit_url)
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")
        name = "Self pickup"
        description = "Pick it up by yourself"
        result = self.client.post(edit_url, {'name': name,
                                             'description': description,
                                             'type': DeliveryTypes.shopper,
                                             'price': 20,
                                             'address_country': self.russian_federation.geonameid,
                                             'address_country__text': u"Россия",
                                             'address_city': self.irkutsk.geonameid,
                                             'address_city__text': u"Иркутск",
                                             'address_street': u"Трудовая",
                                             'address_building': "2",
                                             'address_office': '',
                                             'address_description': "U got some description here, lad",
                                             'address_lat': 52.17,
                                             'address_lon': 104.16})
        self.failUnlessEqual(result.status_code, 302, "This is a correct request which redirects")
        renewed_delivery = Delivery.public_objects.get(id=self.delivery.id)
        self.failUnlessEqual(renewed_delivery.name, name, "Must have changed name")
        self.failUnlessEqual(renewed_delivery.description, description, "Must have changed description")
        self.failUnlessEqual(renewed_delivery.price, 20, "Must have changed price")
        self.failUnlessEqual(int(renewed_delivery.type), DeliveryTypes.shopper, "Must not have changed type")
        self.failUnlessEqual(renewed_delivery.dynamic_properties['address']['text']['street'], u"Трудовая", "Address must be new")
        self.failUnlessEqual(renewed_delivery.dynamic_properties['address']['point']['lat'], 52.17, "Point must be new")

    def test_add_delivery(self):
        add_url = reverse('add_delivery')
        name = "By EMS"
        description = "By mail"
        post = {'name': name,
                'description': description,
                'type': DeliveryTypes.mail,
                'price': 20
                }
        before_deliveries = Delivery.public_objects.all().count()
        result = self.client.post(add_url, post)
        self.failUnlessEqual(result.status_code, 302, "Must have redirect")
        after_deliveries = Delivery.public_objects.all().count()
        self.failUnlessEqual(before_deliveries+1,after_deliveries, "Must have added 1 delivery")
        delivery = Delivery.public_objects.order_by('-id')[0]
        self.failUnlessEqual(delivery.name, name, "Must have this name")

    def test_add_with_text_address(self):
        add_url = reverse('add_delivery')
        name = "By EMS"
        description = "By mail"
        post = {'name': name,
                'description': description,
                'type': DeliveryTypes.mail,
                'price': 20,
                'address_country': self.russian_federation.geonameid,
                'address_city': self.irkutsk.geonameid,
                'address_street': u"Трудовая",
                'address_building': "2",
                'address_office': '',
                'address_description': "U got some description here, lad",
                }
        before_deliveries = Delivery.public_objects.all().count()
        result = self.client.post(add_url, post)
        self.failUnlessEqual(result.status_code, 302, "Must have redirect")
        after_deliveries = Delivery.public_objects.all().count()
        self.failUnlessEqual(before_deliveries + 1,after_deliveries, "Must have added 1 delivery")
        delivery = Delivery.public_objects.order_by('-id')[0]
        self.failUnlessEqual(delivery.name, name, "Must have this name")
        self.failUnlessEqual(unicode(self.russian_federation.geonameid), delivery.dynamic_properties['address']['text']['country'], "Country must be correct")

    def test_add_with_unresolved_address(self):
        add_url = reverse('add_delivery')
        name = "By EMS"
        description = "By mail"
        no_country = u"Сказочная страна"
        no_city = u"Изумрудный город"
        post = {'name': name,
                'description': description,
                'type': DeliveryTypes.mail,
                'price': 20,
                'address_country': no_country,
                'address_city': no_city,
                'address_street': u"Трудовая",
                'address_building': "200",
                'address_office': "321",
                'address_description': "U got some description here, lad",
                }
        before_deliveries = Delivery.public_objects.all().count()
        result = self.client.post(add_url, post)
        self.failUnlessEqual(result.status_code, 302, "Must have redirect")
        after_deliveries = Delivery.public_objects.all().count()
        self.failUnlessEqual(before_deliveries + 1,after_deliveries, "Must have added 1 delivery")
        delivery = Delivery.public_objects.order_by('-id')[0]
        self.failUnlessEqual(delivery.name, name, "Must have this name")
        self.failUnlessEqual(delivery.dynamic_properties['address']['text']['country'], no_country, "Country must be correct")
        self.failUnlessEqual(delivery.dynamic_properties['address']['text']['city'], no_city, "City must be correct")
        result = self.client.get(reverse('show_deliveries'))
        self.failUnlessEqual(result.status_code, 200, "Must be a correct request")

    def test_add_with_point(self):
        add_url = reverse('add_delivery')
        name = "By EMS"
        description = "By mail"
        post = {'name': name,
                'description': description,
                'type': DeliveryTypes.mail,
                'price': 20,
                'address_lat': 52.17,
                'address_lon': 104.16
                }
        before_deliveries = Delivery.public_objects.all().count()
        result = self.client.post(add_url, post)
        self.failUnlessEqual(result.status_code, 302, "Must have redirect")
        after_deliveries = Delivery.public_objects.all().count()
        self.failUnlessEqual(before_deliveries + 1,after_deliveries, "Must have added 1 delivery")
        delivery = Delivery.public_objects.order_by('-id')[0]
        self.failUnlessEqual(delivery.description, description, "Must have this description")
        self.failUnlessEqual(delivery.price, 20, "Must have this price")
        self.failUnlessEqual(int(delivery.type), DeliveryTypes.mail, "Must have this delivery type")
        self.failUnlessEqual(delivery.dynamic_properties['address']['point']['lat'], 52.17, "Latitude must be this one")

# -*- coding: utf-8 -*-

from django_dynamic_fixture import get
from django.core.urlresolvers import reverse
from orders.models import Delivery, DT_BY_SHOPPER
from utils.base_testcase import BaseTestCase
from django.contrib.auth.models import User

class DeliveriesDeleteTestCase(BaseTestCase):
    def setUp(self):
        super(DeliveriesDeleteTestCase, self).setUp()
        self.setGeoNames()
        self.delivery = get(Delivery, name="Pick up yourself",
                            description="Pick it up yourself",
                            type=DT_BY_SHOPPER,
                            price=0)
        self.delivery.save()
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
        
        
    def test_delete_deliveries(self):
        url = reverse('delete_delivery', kwargs={'id': self.delivery.id})
        result = self.client.get(url)
        self.failUnlessEqual(result.status_code, 200, "This is a correct request")

        result = self.client.post(url)
        self.failUnlessEqual(result.status_code, 302, "This is a correct request")
        self.assertRaises(Delivery.DoesNotExist, lambda f: Delivery.objects.get(id=self.delivery.id), "Must be no such delivery")
        self.failUnlessEqual(self.delivery.dynamic_properties.collection.find_one({'_id': 2}), None, "Must be deleted from mongo")
        

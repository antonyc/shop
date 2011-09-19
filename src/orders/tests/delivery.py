# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils import simplejson
from utils.base_testcase import BaseTestCase

class DeliveryTest(BaseTestCase):

    def setUp(self):
        super(DeliveryTest, self).setUp()
        self.setGeoNames()
        self.setUpDelivery()

    def test_get_nearest(self):
        url = reverse('nearest_delivery')
        response = self.client.get(url + '?lon=37.617633&lat=55.755786')
        self.failUnlessEqual(response.status_code, 200, "A correct request")
        simplejson.loads(response.content)
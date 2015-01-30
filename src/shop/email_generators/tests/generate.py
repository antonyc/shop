# -*- coding: utf-8 -*-
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_dynamic_fixture import new, get
from business_events.models import Event
from catalog.models import Item
from orders.models import OrderStatuses, Order
from utils.base_testcase import BaseTestCase


class StatusChanged(BaseTestCase):
    def setUp(self):
        super(StatusChanged, self).setUp()
        self.setUpItems()
        self.setUpOrders()
        self.order_status_changed = get(Event, user=self.user,
                                        notify=True,
                                        sent_at=None)
        order = self.order_status_changed
        order.dynamic_properties['event'] = {'order_id': self.zver_order.id,
                                             'status': {'was': OrderStatuses.new,
                                                        'now': OrderStatuses.processed},
                                             'type': 'order_status_changed'}

    def test_generate(self):
        result = call_command('mail_users', **{'simulate': False,
                                               'verbosity': 2,
                                               'mailto': 'chaporginanton@yandex.ru'})
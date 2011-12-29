# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.core.management import call_command
from utils.base_testcase import BaseTestCase
from orders.models import Order, OrderItem, OrderStatuses, OrderComment
from business_events.models import Event


class FindOrdersToReturnTest(BaseTestCase):
    def setUp(self):
        super(FindOrdersToReturnTest, self).setUp()
        self.setUpOrders()

    def test_management_command(self):
        self.zver_order.till = datetime.now() - timedelta(seconds=10)
        self.zver_order.status = Order.ORDER_STATUSES.delivered
        self.zver_order.save()
        before_command = Event.objects.all().count()
        call_command("find_orders_to_return", verbosity=0)
        self.assertEqual(before_command, Event.objects.all().count() - 1)
        call_command("find_orders_to_return")
        self.assertEqual(before_command, Event.objects.all().count() - 1)

from datetime import timedelta, datetime
from business_events.models import Event
from orders.models import Order
from django.core.management.base import BaseCommand

def is_desired_notification(event, order):
    document = event.dynamic_properties.fetchDocument()
    if (document.get('order') or {}).get('id') == order.id:
        if event.event_type == Event.EVENT_TYPES.time_to_return:
            return True
    return False

class Command(BaseCommand):
    help = """Inspects orders and if it is time to return the order,
generates event 'time_to_return' if it does not exist yet"""
    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity'))
        evs_to_check = Event.objects.filter(created_at__gte=datetime.now() - timedelta(days=1),
                                            notify=True)
        f_kw = {'status': Order.ORDER_STATUSES.delivered,
                'till__lte': datetime.now(),}
        for order in Order.objects.filter(**f_kw):
            if any(is_desired_notification(_, order) for _ in evs_to_check):
                if verbosity > 1:
                    print "already had notification for order", order.id
                continue
            # now create the event, it's missing
            event = Event(notify=True)
            event.save()
            event.dynamic_properties["event"] = {"type": Event.EVENT_TYPES.time_to_return}
            event.dynamic_properties["order"] = {"id": order.id}
            if verbosity > 0:
                print "created event for order", order.id
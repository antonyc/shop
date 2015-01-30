__author__ = 'chapson'
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.translation import activate, ugettext
from email_generators.v1.base import BaseGenerator
from orders.models import Order, OrderStatuses
from django.template.loader import render_to_string


class Generator(BaseGenerator):
    def run(self, events):
        def generator():
            for event in self.events_by_type(events, 'order_status_changed'):
                event_properties = event.dynamic_properties.fetchDocument().get('event', {})
                if event_properties.get('status', {}).get('was', None) is None:
                    continue
                order = Order.objects.select_related('user').\
                    get(id=event_properties.get("order_id"))
                if event_properties.get('author_id') == order.user_id:
                    continue
                profile = order.user.get_profile()
                activate(profile.res_ui_lang)
                subject = ugettext("Order: status changed")
                message =  EmailMessage(subject=subject,
                                        from_email=settings.SERVER_EMAIL,
                                        to=(self.email_name(profile.full_name,
                                                           order.user.email),),
                                        body=self.body(order))
                message.content_subtype = "html"
                yield message
        return generator()

    def body(self, order):
        params = {'order': order,
                  'user': order.user}
        return render_to_string('emails/v1/order_status_changed.html', params)
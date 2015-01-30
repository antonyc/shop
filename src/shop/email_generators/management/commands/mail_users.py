from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from optparse import make_option
from business_events.models import Event
from email_generators import api
__author__ = 'chapson'


class Command(BaseCommand):
    help = "Create and send emails based on events"
    option_list=BaseCommand.option_list + (
        make_option('--simulate','-s',
            action='store_true',
            dest='simulate',
            default=False,
            help='Only generate letters without sending'),
        make_option('--mailto','-m',
            action='store',
            type='string',
            dest='mailto',
            default='',
            help='send every notification to given email'),
        make_option('--keep','-k',
            action='store_true',
            dest='keepletters',
            default=False,
            help='dont mark events as sent'))
    emails_sent = 0
    
    def handle(self, *args, **options):
        self.preset_options(options)
        events = self.events()
        reducing_list_of_events = list(events)
        for api_version, generators in api.iteritems():
            filtered_events = self.reduce_by_api_version(reducing_list_of_events, api_version)
            for generator in generators:
                for email in generator.run(filtered_events):
                    self.send_email(email)
                map(lambda event: reducing_list_of_events.remove(event),
                    generator.trash())
        if not options.get('keepletters'):
            self.mark_events_sent(events)
        if self.verbosity > 1:
            print 'Sent %d emails' % self.emails_sent

    def preset_options(self, options):
        def notify_simulation():
            if self.verbosity > 0 and self.simulate:
                print 'Simulation mode - no real sending!'
        def notify_email_overriden():
            if self.verbosity > 1 and self.mail_to:
                print 'All mails will be sent to', self.mail_to
        self.verbosity = int(options.get('verbosity'))
        self.simulate = options.get('simulate')
        notify_simulation()
        self.mail_to = options.get('mailto')
        notify_email_overriden()

    def send_email(self, email_message):
        self.emails_sent += 1
        if settings.DEBUG:
            email_message.to = map(lambda admin: admin[1], settings.ADMINS)
        if self.mail_to:
            email_message.to = [self.mail_to]
        if self.verbosity > 1:
            print "Sending to", email_message.to
        if not self.simulate:
            email_message.send()

    def events(self):
        return Event.objects.filter(sent_at=None,
                                    notify=True).order_by('created_at')

    def reduce_by_api_version(self, reducing_list, version):
        result = []
        for event in reducing_list:
            if event.dynamic_properties.api_version() == version:
                result.append(event)
                reducing_list.remove(event)
        return result

    def mark_events_sent(self, events):
        events.update(sent_at=datetime.now())
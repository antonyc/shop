# -*- coding:utf-8 -*-
from django.core.management import call_command
import sys
from django.utils.translation import ugettext
from optparse import make_option
from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User

def output(message):
    sys.stdout.write("\n%s " % message)
    sys.stdout.flush()

def input():
    user_input = raw_input().lower()
    if not user_input: return ''
    else: return user_input[0]

class Command(NoArgsCommand):
    help = """Creates superuser if none exists

Use --noinput to suppress input if superuser already exists
    """
    option_list = NoArgsCommand.option_list + (
        make_option('--noinput', action='store_true', dest='noinput', default=False,
                    help="Don't prompt for user input"),
                    )

    def handle_noargs(self, **options):
        superusers = User.objects.filter(is_superuser=True)
        create = False
        if superusers.count() == 0:
            create = True
        else:
            if not options.get('noinput'):
                message = ugettext("You already have a superuser created, do you want to create another one? Type [y/N]")
                output(message)
                user_input = input()
                while user_input not in ('y', 'n', ''):
                    message = ugettext("please use \"y\" or \"n\"")
                    output(message)
                    user_input = input()
                if user_input == 'y':
                    create = True
        if create:
            call_command('createsuperuser')

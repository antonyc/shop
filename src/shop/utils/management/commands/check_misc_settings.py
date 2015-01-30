# -*- coding:utf-8 -*-
from __future__ import with_statement
import sys
import os
import getpass
from django.utils.translation import ugettext
from django.core.management.base import NoArgsCommand
from django.db import connection
from django.conf import settings
from django.db.utils import ConnectionHandler
from yandex_apps import rest_request

secret_settings_path = "/etc/amadika/shop/secret_settings.py"

def output(message):
    sys.stdout.write("%s " % message)
    sys.stdout.flush()

def input():
    return raw_input().lower()

def get_settings_for_write():
    if os.path.exists(secret_settings_path):
        fp = open(secret_settings_path, 'a')
    else:
        fp = open(secret_settings_path, 'w')
        fp.write("#!/usr/bin/env python\n\n")
    return fp


def check_database():
    try:
        connection.cursor()
    except Exception:
        return False
    return True


def check_yandex():
        response = rest_request('http://oauth.yandex.ru/token',
                            data={'grant_type': 'password',
                                  'username': 'chaporginanton',
                                  'password': 'my1NicePass'})

class Command(NoArgsCommand):
    requires_model_validation = False
    help = """Checks your project settings

Checks you database connection settings, mongodb, Yandex Account (Metrika + Maps API key).
"""
#    option_list = NoArgsCommand.option_list + (
#        make_option('--noinput', action='store_true', dest='noinput', default=False,
#                    help="Try not to ask user if possible"),
#                    )

    def handle_noargs(self, **options):
        self.verbosity = options.get('verbosity')
        self.noinput = options.get('noinput')
        database_config = not check_database()
        if self.verbosity > 0 and not database_config:
            print ugettext("Your database connection is OK")
        yandex_config = False
        
        if database_config or yandex_config:
            output(ugettext("The script will setup secret_settings.py into '%s'") % secret_settings_path)
        if database_config:
            try:
                self.database_config()
            except KeyboardInterrupt:
                print "\n\nInterrupted by you, leaving this installation unconfigured!"

    def yandex_services(self):
        pass

    def database_config(self):
        def prompt_for_string(message, nonempty=None, input_callable=None):
            if input_callable is None:
                input_callable = raw_input
            output(message)
            result = input_callable()
            if not result:
                if nonempty is not None:
                    while not result:
                        output(nonempty)
                        result = input_callable()
            return result

        def prompt():
            name = prompt_for_string("\n" + ugettext("1) please type in your database name:"),
                                     ugettext("database name can not be blank:"))
            user = prompt_for_string(ugettext("2) type in database user name:"),
                                     ugettext("database user name cannot be blank:"))
            password = prompt_for_string(ugettext("3) type in '%s's" % user),
                                         ugettext("password cannot be blank:"),
                                         getpass.getpass)
            host = prompt_for_string(ugettext("4) type in database host [leave empty for default]:"))
            port = prompt_for_string(ugettext("5) type in database port [leave empty for default]:"))
            DATABASES = {'custom': DATABASE_TEMPLATE['default'].copy() }
            DATABASES['custom'].update({'NAME': name,
                                        'USER': user,
                                        'PASSWORD': password,
                                        'HOST': host,
                                        'PORT': port})
            connections = ConnectionHandler(DATABASES)
            test_connection_wrapper = connections['custom']
            try:
                test_connection_wrapper.cursor()
                return DATABASES['custom']
            except Exception:
                print ugettext("It seems that you provided incorrect settings. Try again, please.")

        output("\n" + ugettext("Database setup. You should have created the database in advance. You will be asked to input 5 strings:"))
        db_settings = prompt()
        while not db_settings:
            db_settings = prompt()
        final_settings = DATABASE_TEMPLATE['default'].copy()
        for key in final_settings:
            if key in db_settings:
                final_settings[key] = db_settings[key]
        with get_settings_for_write() as fp:
            fp.write("\n\nDATABASES = " + repr({'default': final_settings}))
        print ugettext("Database settings saved. It's OK!")


DATABASE_TEMPLATE = { 'default': settings.DATABASES['default'].copy() }
#        {
#        'ENGINE': 'django.contrib.gis.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'amadika_shop',                      # Or path to database file if using sqlite3.
#        'USER': 'shop_admin1',                      # Not used with sqlite3.
#        'PASSWORD': 'password',                  # Not used with sqlite3.
#        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#        'TEST_CHARSET': 'utf8',
#        'TEST_COLLATION': 'utf8_general_ci',
#        'OPTIONS': {
#            'init_command': 'SET storage_engine=INNODB; SET names utf8;'
#        },
#    }


YANDEX_TEMPLATE = settings.YANDEX.copy()
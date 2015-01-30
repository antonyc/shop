import datetime, gzip, os, sys, zipfile
from optparse import make_option

from django.core.management.base import BaseCommand

from geonames import models
GEONAMES_DATA = os.path.abspath(os.path.join(os.path.dirname(models.__file__), 'data'))

class Command(BaseCommand):
    def handle(self, **options):
        pass
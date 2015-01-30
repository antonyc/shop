import datetime, gzip, os, sys, zipfile
from optparse import make_option

from django.core.management.base import BaseCommand

from geonames import models
GEONAMES_DATA = os.path.abspath(os.path.join(os.path.dirname(models.__file__), 'data'))

class Command(BaseCommand):
    def handle(self, **options):
        command = """zcat %(geonames)s | sed -e "s/\\\//g" | sed -e "s/\"/\\\\\"/g" | sed -e "s/^\([^\t]*\)\t\([^\t]*\)\t[^\t]*\t\([^\t]*\)\t\([^\t]*\)*\t\([^\t]*\)\t\([AP][^\t]*\)\t\([^\t]*\)\t\([^\t]*\)\t\(.*\)$/INSERT INTO geonames_geoname (geonameid, name, alternates, point, fclass, fcode, country, cc2, admin1, admin2, admin3, admin4, population, timezone, moddate) VALUES (\1, \"\2\", \"\", POINT(\4, \5), \"\6\", \"\7\", \"\8\", ----\9/g" | sed -e "s/^[^\(INSERT\)].*//" | sed -e "s/^\([^\t]*\) ----\([^\t]*\)\t\([^\t]*\)\t\([^\t]*\)\t\([^\t]*\)\t\([^\t]*\)\t\([^\t]*\)\t[^\t]*\t[^\t]*\t\([^\t]*\)\t\([^\t]*\).*/\1 \"\2\", \"\3\", \"\4\", \"\5\", \"\6\", \"\7\", \"\8\", \"\9 00:00:00\");/g"
        """ % {'path': os.path.join(GEONAMES_DATA, 'allCountries.gz')}
        os.system(command)
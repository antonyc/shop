from django.db import models
# Create your models here.
from collections import namedtuple
geo_place_types = ('country', 'city')
GeoPlaceType = namedtuple('GeoPlaceType', ' '.join(geo_place_types))._make((1, 4))
GEOMODEL_TYPES = [(GeoPlaceType.country, geo_place_types[0]),
                  (GeoPlaceType.city, geo_place_types[1])]

class Geomodel(models.Model):
    typ = models.PositiveSmallIntegerField(choices=GEOMODEL_TYPES, blank=False)
    geonameid = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True, blank=False)
    population = models.PositiveIntegerField(default=0)
    country_code = models.CharField(max_length=3, blank=False)
    
    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.country_code)

class Geoalternate(models.Model):
    geoname = models.ForeignKey(Geomodel)
    variant = models.CharField(max_length=200, db_index=True, blank=True)
    isolanguage = models.CharField(max_length=3)
    preferred = models.BooleanField(default=False)
    short = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u"%s \"%s\" of \"%s\"" % (self.isolanguage, self.variant, self.geoname.name)
    
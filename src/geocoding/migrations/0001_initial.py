# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Geomodel'
        db.create_table('geocoding_geomodel', (
            ('typ', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('geonameid', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('population', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('geocoding', ['Geomodel'])

        # Adding model 'Geoalternate'
        db.create_table('geocoding_geoalternate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geoname', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geocoding.Geomodel'])),
            ('variant', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=200, blank=True)),
            ('isolanguage', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('preferred', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('short', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('geocoding', ['Geoalternate'])

    def backwards(self, orm):
        
        # Deleting model 'Geomodel'
        db.delete_table('geocoding_geomodel')

        # Deleting model 'Geoalternate'
        db.delete_table('geocoding_geoalternate')

    models = {
        'geocoding.geoalternate': {
            'Meta': {'object_name': 'Geoalternate'},
            'geoname': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geocoding.Geomodel']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isolanguage': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'preferred': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'short': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'variant': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'})
        },
        'geocoding.geomodel': {
            'Meta': {'object_name': 'Geomodel'},
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'geonameid': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'population': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'typ': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['geocoding']

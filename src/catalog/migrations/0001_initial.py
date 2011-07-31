# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('catalog_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Category'], null=True)),
        ))
        db.send_create_signal('catalog', ['Category'])

        # Adding model 'Item'
        db.create_table('catalog_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('catalog', ['Item'])

        # Adding model 'ItemImage'
        db.create_table('catalog_itemimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alt', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('catalog', ['ItemImage'])

    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('catalog_category')

        # Deleting model 'Item'
        db.delete_table('catalog_item')

        # Deleting model 'ItemImage'
        db.delete_table('catalog_itemimage')

    models = {
        'catalog.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Category']", 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'catalog.item': {
            'Meta': {'object_name': 'Item'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'catalog.itemimage': {
            'Meta': {'object_name': 'ItemImage'},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['catalog']

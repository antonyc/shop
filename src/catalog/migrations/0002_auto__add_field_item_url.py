# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Item.url'
        db.add_column('catalog_item', 'url', self.gf('django.db.models.fields.CharField')(default='random', unique=True, max_length=255), keep_default=False)

        # Adding M2M table for field categories on 'Item'
        db.create_table('catalog_item_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm['catalog.item'], null=False)),
            ('category', models.ForeignKey(orm['catalog.category'], null=False))
        ))
        db.create_unique('catalog_item_categories', ['item_id', 'category_id'])

    def backwards(self, orm):
        
        # Deleting field 'Item.url'
        db.delete_column('catalog_item', 'url')

        # Removing M2M table for field categories on 'Item'
        db.delete_table('catalog_item_categories')

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
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['catalog.Category']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'catalog.itemimage': {
            'Meta': {'object_name': 'ItemImage'},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['catalog']

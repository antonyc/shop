# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Item.created_at'
        db.add_column('catalog_item', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default='2011-07-31 15:14:20', blank=True), keep_default=False)

        # Adding field 'ItemImage.created_at'
        db.add_column('catalog_itemimage', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default='2011-07-31 15:14:20', blank=True), keep_default=False)

        # Adding field 'Category.created_at'
        db.add_column('catalog_category', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default='2011-07-31 15:14:20', blank=True), keep_default=False)

    def backwards(self, orm):
        
        # Deleting field 'Item.created_at'
        db.delete_column('catalog_item', 'created_at')

        # Deleting field 'ItemImage.created_at'
        db.delete_column('catalog_itemimage', 'created_at')

        # Deleting field 'Category.created_at'
        db.delete_column('catalog_category', 'created_at')

    models = {
        'catalog.category': {
            'Meta': {'object_name': 'Category'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Category']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'catalog.item': {
            'Meta': {'object_name': 'Item'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['catalog.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'catalog.itemimage': {
            'Meta': {'object_name': 'ItemImage'},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['catalog']

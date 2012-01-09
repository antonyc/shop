# -*- coding: utf-8 -*-

import os
from django.conf import settings
from django.db import models
from mptt.models import MPTTModel
from utils.images import Thumbnail


class Category(MPTTModel):
    name = models.CharField(max_length=255, blank=False)
    url = models.CharField(max_length=255, blank=False, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"\"%s\" %s" % (self.url or '', self.name or '')

    @property
    def all_items(self):
        ids = map(lambda value: value[0],
                  self.get_descendants(True).values_list('id'))
        return Item.public_objects.filter(categories__in=ids)

    @property
    def has_items(self):
        return self.all_items.exists()


class ItemDefaulManager(models.Manager):
    def main_image(self, item):
        image = item.itemimage_set.all().order_by('created_at')
        if not image.exists():
            return False
        main_image = image[0]
        return main_image

class ItemPublicManager(ItemDefaulManager):
    def get_query_set(self):
        return super(ItemPublicManager, self).get_query_set().filter(hidden=False,deleted=False)

class Item(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False)
    formatted_description = models.TextField(blank=True)
    url = models.CharField(max_length=255, blank=False, unique=True)
    categories = models.ManyToManyField(Category, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hidden = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    price = models.FloatField(blank=False)
    
    public_objects = ItemPublicManager()
    objects = ItemDefaulManager()

    def has_images(self):
        return Item.public_objects.main_image(self)

    def __unicode__(self):
        print u"%s: %s" % (self.id or 'None', self.name[:40] or 'None')



class ItemImage(models.Model):
    alt = models.CharField(max_length=255, blank=False)
    image = models.ImageField(upload_to=os.path.join(settings.UPLOAD_PATH, 'item_image'))
    created_at = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, blank=False)
    
    thumbnail = Thumbnail()
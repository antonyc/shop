# -*- coding: utf-8 -*-

import os
from PIL import Image
from django.conf import settings
from django.db import models
from catalog_utils.model_fields import PreviewImageField
from django.utils.translation import ugettext
from mptt.models import MPTTModel


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
        return Item.objects.filter(categories__in=ids)

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

def gen_thumbnail(field, thumbnail_size):
    thumb_path = os.path.join(settings.MEDIA_ROOT,
                              os.path.dirname(field.name),
                              '%d_%d' % thumbnail_size,
                              os.path.basename(field.name))
    if not os.path.exists(thumb_path):
        try:
            os.makedirs(os.path.dirname(thumb_path))
        except OSError:
            pass
        fp = open(settings.MEDIA_ROOT+'/'+field.name)
        image = Image.open(fp)
        img_ratio = float(field.width) / field.height
        x, y = thumbnail_size
        if x==0.0:
            x = y * img_ratio
        elif y==0.0:
            y = x / img_ratio

        # output file ratio
        resize_ratio = float(x) / y
        x = int(x); y = int(y)

        # get output with and height to do the first crop
        if(img_ratio > resize_ratio):
            output_width = x * image.size[1] / y
            output_height = image.size[1]
            originX = image.size[0] / 2 - output_width / 2
            originY = 0
        else:
            output_width = image.size[0]
            output_height = y * image.size[0] / x
            originX = 0
            originY = image.size[1] / 2 - output_height / 2

        #crop
        cropBox = (originX, originY, originX + output_width, originY + output_height)
        image = image.crop(cropBox)

        # resize (doing a thumb)
        image.thumbnail(thumbnail_size, Image.ANTIALIAS)
        fp.close()
        fp = open(thumb_path, 'w')
        image.save(fp, 'JPEG', quality=90)
        fp.close()
    return settings.MEDIA_URL + thumb_path[len(settings.MEDIA_ROOT)+1:]


class Thumbnail(object):
    def __init__(self, image_field = 'image', thumbnail_size = None):
        self.image_field = image_field
        self.thumbnail_size = thumbnail_size or settings.THUMBNAIL_SIZE
        
    def __get__(self, obj, cls=None):
        field = getattr(obj, self.image_field)
        size = self.thumbnail_size
        return gen_thumbnail(field, size)


class ItemImage(models.Model):
    alt = models.CharField(max_length=255, blank=False)
    image = models.ImageField(upload_to=os.path.join(settings.UPLOAD_PATH, 'item_image'))
    created_at = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, blank=False)
    
    thumbnail = Thumbnail()
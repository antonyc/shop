import os
from PIL import Image
from django.conf import settings
from django.db import models
from catalog.utils.model_fields import PreviewImageField
from django.utils.translation import ugettext
from mptt.models import MPTTModel


class Category(MPTTModel):
    name = models.CharField(max_length=255, blank=False)
    url = models.CharField(max_length=255, blank=False, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    
class Item(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False)
    url = models.CharField(max_length=255, blank=False, unique=True)
    categories = models.ManyToManyField(Category, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hidden = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        print u"%s: %s" % (self.id, self.name[:40])

class Thumbnail(object):
    def __init__(self, image_field = 'image', thumbnail_size = None):
        self.image_field = image_field
        self.thumbnail_size = thumbnail_size or settings.THUMBNAIL_SIZE
        
    def __get__(self, obj, cls=None):
        field = getattr(obj, self.image_field)
        thumb_path = os.path.join(settings.MEDIA_ROOT,
                                  os.path.dirname(field.name), 
                                  '%d_%d' % self.thumbnail_size, 
                                  os.path.basename(field.name))
        if not os.path.exists(thumb_path):
            try:
                os.makedirs(os.path.dirname(thumb_path))
            except OSError:
                pass
#            print settings.MEDIA_ROOT+field.name
            fp = open(settings.MEDIA_ROOT+'/'+field.name)
            image = Image.open(fp)
            img_ratio = float(field.width) / field.height
            x, y = self.thumbnail_size
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
            image.thumbnail(self.thumbnail_size, Image.ANTIALIAS)
            fp.close()
            fp = open(thumb_path, 'w')
            image.save(fp, 'JPEG', quality=90)
            fp.close()
        return settings.MEDIA_URL + thumb_path[len(settings.MEDIA_ROOT)+1:]

class ItemImage(models.Model):
    alt = models.CharField(max_length=255, blank=False)
    image = models.ImageField(upload_to=os.path.join(settings.UPLOAD_PATH, 'item_image'))
    created_at = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, blank=False)
    
    thumbnail = Thumbnail()
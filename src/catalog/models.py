from django.conf import settings
from django.db import models
from catalog.utils.model_fields import PreviewImageField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, blank=False)
    url = models.CharField(max_length=255, blank=False, unique=True)
    parent = models.ForeignKey('self', null=True)
    
class Item(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False)

class ItemImage(models.Model):
    alt = models.CharField(max_length=255, blank=False)
    image = PreviewImageField(upload_to=settings.UPLOAD_PATH)
    
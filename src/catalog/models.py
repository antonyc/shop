from django.db import models
from catalog.utils.model_fields import PreviewImageField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, required=True)
    url = models.CharField(max_length=255, required=True, db_index=True)
    parent = models.ForeignKey('self', null=True)
    
class Item(models.Model):
    name = models.CharField(max_length=255, required=True)
    description = models.TextField(required=True)

class ItemImage(models.Model):
    alt = models.CharField(max_length=255, required=True)
    image = PreviewImageField()
    
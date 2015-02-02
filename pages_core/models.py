# coding: utf-8

from django.db import models


class Page(models.Model):
    url = models.CharField(max_length=2000, unique=True)
    body = models.TextField()
    formatted_body = models.TextField()
    title = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

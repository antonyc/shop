# -*- coding: utf-8 -*-

import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from utils.strings import translit
from utils.images import Thumbnail

class Page(models.Model):
    author = models.ForeignKey(User, blank=False)
    url = models.CharField(max_length=254, blank=False, unique=True)
    body = models.TextField(blank=False)
    formatted_body = models.TextField(blank=True)
    title = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_user = models.CharField(max_length=255, blank=False)

    def make_url(self):
        self.url = None
        translitted_title = translit(self.title).lower()
        url = translitted_title
        cnt = 1
        while self.url is None:
            try:
                Page.objects.get(url=url)
                url = u'%s_%s' % (translitted_title, cnt)
                cnt += 1
            except Page.DoesNotExist:
                self.url = url
        return self.url
    
    def __unicode__(self):
        return u'%s: %s' % (self.url[:50], self.title[:20])


class PageImage(models.Model):
    alt = models.CharField(max_length=255, blank=False)
    image = models.ImageField(upload_to=os.path.join(settings.UPLOAD_PATH, 'page_image'))
    created_at = models.DateTimeField(auto_now_add=True)
    page = models.ForeignKey(Page, blank=True, null=True)

    thumbnail = Thumbnail()

class RedirectPage(models.Model):
    from_url = models.CharField(max_length=254, blank=False, unique=True)
    to_page = models.ForeignKey(Page, blank=False)
    
    def __unicode__(self):
        return u'%s to %s' % (self.from_url, self.to_page.url)
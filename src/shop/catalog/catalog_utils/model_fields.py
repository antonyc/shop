# -*- coding: utf-8 -*-
'''
Created on 31.07.2011

@author: chapson
'''
from django.db import models

class PreviewImageField(models.ImageField):
    def generate_preview(self, max_side):
        assert isinstance(max_side, int), True
        
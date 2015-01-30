# -*- coding: utf-8 -*-
from pages.models import PageImage
from utils.forms import AmadikaModelForm

__author__ = 'chapson'

class PageImageForm(AmadikaModelForm):
    class Meta:
        model = PageImage
        exclude = ('page',)


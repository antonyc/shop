# coding: utf-8

from django.views import generic

from pages_core.models import Page


class PageView(generic.DetailView):
    model = Page
    template_name = 'pages_public/page_detail.html'

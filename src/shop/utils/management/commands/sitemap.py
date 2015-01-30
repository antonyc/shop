# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from pages.models import Page
from django.core.management.base import BaseCommand
from optparse import make_option
from lxml import etree
__author__ = 'chapson'

now = datetime.now()
class Command(BaseCommand):
    help = "Generate sitemap and print to STDOUT"
    option_list=BaseCommand.option_list + (
        make_option('--pages','-p',
            action='store',
            type='int',
            dest='pages',
            default=100,
            help='How many pages shall be in sitemap'),
        make_option('--output','-o',
            action='store',
            type='string',
            dest='output',
            default='/usr/share/amadika/shop/media/sitemap.xml',
            help='Where to put the generated file'),
        )

    def handle(self, *args, **options):
        self.verbosity = int(options.get('verbosity'))
        urlset = []
        self.pages(urlset, options.get('pages'))
        fp = open(options.get('output'), 'w')
        fp.write(render_to_string('sitemap.xml', {'urlset': urlset}))
        fp.close()

    def pages(self, urlset, number):
        qs = Page.objects.only('url', 'updated_at').order_by('-updated_at')
        if number > 0:
            qs = qs[:number]
        for page in qs:
            priority = 0
            lower_priority_window = now - timedelta(days=100)
            if page.updated_at > lower_priority_window:
                priority = round((page.updated_at - lower_priority_window).days / 100.0, 1)
            urlset.append({'location': '/page/' + page.url,
                           'lastmod': page.updated_at,
                           'changefreq': 'weekly',
                           'priority': priority})

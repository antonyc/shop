# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from administration.views import AdminTemplateView
from utils import site_settings
from utils.menu import parse_menu, build_menu

__author__ = 'chapson'


def default_filter(obj):
    return obj


filters = {'top_menu': parse_menu}


class ParseMenuText(AdminTemplateView):
    def get(self, request, *args, **kwargs):
        if not request.is_ajax:
            return HttpResponse(status=500)
        menu = parse_menu(request.GET.get('text', ''))
        return HttpResponse(", ".join(build_menu(menu['parsed'])))


class ShowSettingsView(AdminTemplateView):
    template_name = 'site_configuration/show.html'
    def get(self, request, *args, **kwargs):
        self.params['site_settings'] = site_settings
        return self.render_to_response(self.params)

    def post(self, request, *args, **kwargs):
        settings = {}
        for key in request.POST:
            if key == 'csrfmiddlewaretoken':
                continue
            processor = filters.get(key, default_filter)
            site_settings[key] = processor(request.POST.get(key))
        return HttpResponseRedirect(reverse('show_settings'))


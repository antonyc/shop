# -*- coding: utf-8 -*-

from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

class BaseTemplateView(TemplateView):
    def dispatch(self, *args, **kwargs):
        self.request = args[0]
        return super(BaseTemplateView, self).dispatch(*args, **kwargs)
    
    def render_to_response(self, context, **response_kwargs):
        if context is not None:
            context['request'] = self.request
        return super(BaseTemplateView, self).render_to_response(context, **response_kwargs)
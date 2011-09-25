# Create your views here.

from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from utils import is_staff

class AdminListView(ListView):
    @method_decorator(user_passes_test(is_staff))
    def dispatch(self, *args, **kwargs):
        self.request = args[0]
        return super(AdminListView, self).dispatch(*args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        context['request'] = self.request
        return super(AdminListView, self).render_to_response(context, **response_kwargs)

class AdminTemplateView(TemplateView):
    params = {}
    @method_decorator(user_passes_test(is_staff))
    def dispatch(self, *args, **kwargs):
        self.request = args[0]
        if self.request.META.get('HTTP_X_REQUESTED_WITH'):
            self.request.is_ajax = True
        else:
            self.request.is_ajax = False
        return super(AdminTemplateView, self).dispatch(*args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        context['request'] = self.request
        return super(AdminTemplateView, self).render_to_response(context, **response_kwargs)
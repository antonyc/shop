# Create your views here.
from utils.base_view import BaseTemplateView
from pages.models import Page
from django.http import Http404


class ShowPageView(BaseTemplateView):
    template_name = 'pages/show.html'
    count_visits = True

    def get(self, request, url, *args, **kwargs):
        try:
            page = Page.objects.get(url=url)
        except Page.DoesNotExist:
            return Http404()
        params = {'page': page}
        return self.render_to_response(params)


class ShowPagesView(BaseTemplateView):
    template_name = 'pages/list.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response(dict(
            pages=Page.objects.order_by('-created_at')[:20]
        ))

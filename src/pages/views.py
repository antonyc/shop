# Create your views here.
from utils.base_view import BaseTemplateView
from pages.models import Page
from django.http import Http404

class ShowPageView(BaseTemplateView):
    template_name = 'pages/show.html'
    def get(self, request, url, *args, **kwargs):
        try:
            page = Page.objects.get(url=url)
        except Page.DoesNotExist:
            return Http404()
        params = {'page': page}
        return self.render_to_response(params)
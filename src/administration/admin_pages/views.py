'''
Created on 31.07.2011

@author: chapson
'''
from django.conf import settings
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.utils.translation import ugettext
from django.core.paginator import Paginator
from pages.models import Page, RedirectPage
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.forms.models import ModelForm
from django.utils import simplejson
from utils.strings import parse_markup
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from utils import is_staff

class PageForm(ModelForm):
    class Meta:
        model = Page
        fields = ('body', 'title')

class EditPageView(TemplateView):
    template_name = 'catalog/page_edit.html'

    @method_decorator(user_passes_test(is_staff))
    def dispatch(self, *args, **kwargs):
#        print 'user'
        return super(EditPageView, self).dispatch(*args, **kwargs)
    
    def get(self, request, id=None, *args, **kwargs):
        params = {}
        if id is None:
            page = Page(author=request.user,)
        else:
            try:
                page = Page.objects.get(id=id)
            except Page.DoesNotExist:
                raise Http404()
        form = PageForm(request.POST,
                        instance=page)
        params['form'] = form
        return self.render_to_response(params)
    
    def post(self, request, id=None, *args, **kwargs):
        params = {}
        if id is None:
            page = Page(author=request.user,)
        else:
            try:
                page = Page.objects.get(id=id)
            except Page.DoesNotExist:
                raise Http404()
        previous_title = page.title
        form = PageForm(request.POST,
                        instance=page)
        if form.is_valid():
            page.title = form.cleaned_data['title']
            if previous_title != page.title:
                if page.id:
                    RedirectPage(from_url=page.url, to_page=page).save()
                page.make_url()
            body = form.cleaned_data['body']
            page.formatted_body = parse_markup(body)
            page.last_user = request.user.username
            page.save()
            return HttpResponseRedirect(reverse('list_pages'))
        else:
            params['form'] = form
            return self.render_to_response(params)


class ListPagesView(ListView):
    template_name = 'catalog/page_list.html'
    model = Page
    queryset = Page.objects.all().order_by('-created_at')
    paginate_by = 50
    allow_empty = True
    
    @method_decorator(user_passes_test(is_staff))
    def dispatch(self, *args, **kwargs):
#        print 'user'
        return super(ListPagesView, self).dispatch(*args, **kwargs)
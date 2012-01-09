# -*- coding: utf-8 -*-
'''
Created on 31.07.2011

@author: chapson
'''
import os
import simplejson
from django.conf import settings
from .forms import PageImageForm
from pages.models import Page, RedirectPage, PageImage
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.forms.models import ModelForm
from utils.forms import AmadikaModelForm
from utils.strings import parse_markup
from administration.views import AdminTemplateView, AdminListView
from administration.admin_pages.tests.parser import BODY_LINKED

class PageForm(AmadikaModelForm):
    class Meta:
        model = Page
        fields = ('title', 'body', )

class EditPageView(AdminTemplateView):
    template_name = 'catalog/page_edit.html'

    def get(self, request, id=None, *args, **kwargs):
        params = {}
        if id is None:
            page = Page(author=request.user,)
        else:
            try:
                page = Page.objects.get(id=id)
            except Page.DoesNotExist:
                raise Http404()
            self.params["images"] = page.pageimage_set.all()
        form = PageForm(instance=page)
        self.params['form'] = form
        self.params['page'] = page
        self.params['image_form'] = PageImageForm(instance=PageImage(page=page))
        return self.render_to_response(self.params)
    
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
            page.body = body
            page.formatted_body = parse_markup(body.replace("\r\n", "\n").strip(), page.title)
            page.last_user = request.user.username
            page.save()
            return HttpResponseRedirect(reverse('list_pages'))
        else:
            params['form'] = form
            return self.render_to_response(params)


class ListPagesView(AdminListView):
    template_name = 'catalog/page_list.html'
    model = Page
    queryset = Page.objects.all().order_by('-created_at')
    paginate_by = 50
    allow_empty = True

class UploadPageImageView(AdminTemplateView):
    params = {}
    def post(self, request, id, *args, **kwargs):
        try:
            page = Page.objects.get(id=id)
        except Page.DoesNotExist:
            raise Http404()

        form = PageImageForm(request.POST, request.FILES,
                             instance=PageImage(page=page))
        if form.is_valid():
            page_image = form.save()
            if not request.is_ajax():
                return HttpResponseRedirect(reverse('edit_page', args=[page.id]))
            result = {'id': page_image.id,
                      'page_id': page_image.page.id,
                      'src': os.path.join(settings.MEDIA_URL, page_image.image.name,),
                      }
            status = 200
        else:
            result = {'fields': form.errors}
            status = 409
        return HttpResponse(simplejson.dumps(result),
                            status=status,
                            mimetype='application/json')


class DeletePageImageView(AdminTemplateView):
    params = {}

    def post(self, request, id, *args, **kwargs):
        try:
            page_image = PageImage.objects.get(id=id)
        except PageImage.DoesNotExist:
            raise Http404()
        id = page_image.page_id
        page_image.delete()
        return HttpResponseRedirect(reverse('edit_page', args=(id,)))
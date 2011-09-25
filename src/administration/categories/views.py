# -*- coding: utf-8 -*-
'''
Created on 31.07.2011

@author: chapson
'''
from catalog.models import Item, Category
from django.utils.translation import ugettext
from django.forms import Form, fields
from django.forms.widgets import Textarea
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template.defaulttags import url
from django.core.urlresolvers import reverse
from utils.strings import translit
from administration.views import AdminListView, AdminTemplateView

class ViewMixin(object):
    errors = []
    def add_error(self, error):
        self.errors.append(error)
    
    def render_error(self, *args):
        for error in args:
            self.add_error(error)
        context = self.get_context_data()
        context['errors'] = self.errors
        return self.render_to_response(context)

class ListCategoriesView(AdminListView):
    model = Category
    queryset = Category.objects.order_by('lft')
    paginate_by = 50
    allow_empty = True

def categories_choices(no=None):
    result = [('', ugettext('No parent'))]
    result += map(lambda cat: (cat.id, cat.name),
                 Category.objects.all().exclude(id=no))
    return result

class EditForm(Form):
    name = fields.CharField(max_length=255, label=ugettext("Name"))
    parent = fields.ChoiceField(choices=(),
                                         label=ugettext("Parent category"), 
                                         required=False)
    def __init__(self, *args, **kwargs):
        category_id = kwargs.pop('category_id', None)
        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['parent'].choices = categories_choices()

class EditCategoryView(AdminTemplateView):
    template_name = 'catalog/category_edit.html'
    params = {}
    
    def get(self, request, id=None, *args, **kwargs):
        if id is None:
            category = Category()
            list = []
        else:
            try:
                category = Category.objects.get(id=id)
            except Category.DoesNotExist:
                raise Http404()
        initial = {'name': category.name,}
        if category.parent_id:
            initial['parent'] = category.parent_id
        form = EditForm(initial=initial)
        
        self.params['form'] = form
        return self.render_to_response(self.params)
    
    def post(self, request, id=None, *args, **kwargs):
        if id is None:
            category = Category()
            category_id = None
        else:
            try:
                category = Category.objects.get(id=id)
                category_id = category.id
            except Item.DoesNotExist:
                raise Http404()
        form = EditForm(request.POST)
        if form.is_valid():
            category.name = form.cleaned_data['name']
            cnt = 0
            url = translit(category.name)
            if not category.id:
                # dont change url for existing categories
                category.url = None
                while category.url is None:
                    try:
                        Category.objects.get(url=url)
                        cnt += 1
                        url = translit(category.name) + str(cnt)
                    except Category.DoesNotExist:
                        category.url = url.lower()
            
            parent_category = None
            if form.cleaned_data['parent']:
                try:
                    parent_category = Category.objects.get(id=form.cleaned_data['parent'])
                except Category.DoesNotExist:
                    pass
            category.parent = parent_category
            category.save()
            return HttpResponseRedirect(reverse('list_categories'))
        else:
            self.params['form'] = form
            return self.render_to_response(self.params, status=409)
        
class DeleteCategoryView(AdminTemplateView):
    template_name = 'catalog/category_delete.html'
    params = {}

    def get(self, request, id):
        try:
            item = Item.objects.get(id=id)
        except Item.DoesNotExist:
            raise Http404()
        self.params['item'] = item
        return self.render_to_response(self.params)
    
    def post(self, request, id):
        try:
            item = Item.objects.get(id=id)
        except Item.DoesNotExist:
            raise Http404()
        item.delete()
        return HttpResponseRedirect(reverse('list_items'))
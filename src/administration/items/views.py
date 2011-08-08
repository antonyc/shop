'''
Created on 31.07.2011

@author: chapson
'''
from django.conf import settings
from catalog.models import Item, Category, ItemImage
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.utils.translation import ugettext
from django.forms import Form, fields
from django.forms.widgets import Textarea
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template.defaulttags import url
from django.core.urlresolvers import reverse
from utils.strings import translit
from administration.categories.views import categories_choices
from administration.images.views import ItemImageForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from utils import is_staff

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

class ListItemsView(ListView):
    model = Item
    queryset = Item.objects.all().order_by('-created_at')
    paginate_by = 50
    allow_empty = True 

    @method_decorator(user_passes_test(is_staff))
    def dispatch(self, *args, **kwargs):
        return super(ListItemsView, self).dispatch(*args, **kwargs)


class EditForm(Form):
    name = fields.CharField(max_length=255, label=ugettext("Name"))
    description = fields.Field(widget=Textarea, required=True, label=ugettext("Description"))
    categories = fields.MultipleChoiceField(choices=(), 
                                            label=ugettext("Categories"), 
                                            required=False)
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['categories'].choices = categories_choices()

class EditItemsView(TemplateView):
    template_name = 'catalog/item_edit.html'
    params = {}

    @method_decorator(user_passes_test(is_staff))
    def dispatch(self, *args, **kwargs):
        return super(EditItemsView, self).dispatch(*args, **kwargs)

    def get(self, request, id=None, *args, **kwargs):
        if id is None:
            item = Item()
            list = []
        else:
            try:
                item = Item.objects.select_related(depth=1).get(id=id)
                list = map(lambda c: c.id, item.categories.all())
            except Item.DoesNotExist:
                raise Http404()
        form = EditForm(initial={'name': item.name,
                                 'description': item.description,
                                 'categories': list})
        self.params['form'] = form
        self.params['image_form'] = ItemImageForm(instance=ItemImage(item=item))
        images = []
        for image in item.itemimage_set.all():
            images.append({'url': settings.MEDIA_URL + image.image.name,
                           'alt': image.alt,
                           'object': image,})
        self.params['images'] = images
        self.params['item'] = item
#        context.update(self.params)
        return self.render_to_response(self.params)
    
    def post(self, request, id=None, *args, **kwargs):
        if id is None:
            item = Item()
        else:
            try:
                item = Item.objects.get(id=id)
            except Item.DoesNotExist:
                raise Http404()
        form = EditForm(request.POST)
        if form.is_valid():
            item.name = form.cleaned_data['name']
            item.description = form.cleaned_data['description']
            cnt = 0
            url = translit(item.name).lower()
            if not item.id:
                # dont change url for existing items
                item.url = None
                while item.url is None:
                    try:
                        Item.objects.get(url=url)
                        cnt += 1
                        url = translit(item.name).lower() + str(cnt)
                    except Item.DoesNotExist:
                        item.url = url
            item.save()
            item.categories = Category.objects.filter(id__in=form.cleaned_data['categories'])
            item.save()
            return HttpResponseRedirect(reverse('list_items'))
        else:
            self.params['form'] = form
            return self.render_to_response(self.params, status=409)
        
class DeleteItemsView(TemplateView):
    template_name = 'catalog/item_delete.html'
    params = {}

    @method_decorator(user_passes_test(is_staff))
    def dispatch(self, *args, **kwargs):
        return super(DeleteItemsView, self).dispatch(*args, **kwargs)

    
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
# -*- coding: utf-8 -*-
'''
Created on 31.07.2011

@author: chapson
'''
from catalog.models import Item, Category, ItemImage
from django.utils.translation import ugettext
from django.forms import Form, fields
from django.forms.widgets import Textarea
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template.defaulttags import url
from django.core.urlresolvers import reverse
from utils.strings import translit
from django.forms.models import ModelForm
from django.utils import simplejson
from django.conf import settings
import os
from administration.views import AdminTemplateView

class ItemImageForm(ModelForm):
    class Meta:
        model = ItemImage
        exclude = ('item',)

class UploadItemImageView(AdminTemplateView):
    params = {}
    def post(self, request, id, *args, **kwargs):
        try:
            item = Item.objects.get(id=id)
        except Item.DoesNotExist:
            raise Http404()

        form = ItemImageForm(request.POST, request.FILES, 
                             instance=ItemImage(item=item))
        if form.is_valid():
            item_image = form.save()
            if not request.is_ajax():
                return HttpResponseRedirect(reverse('edit_item', args=[item.id])) 
            result = {'id': item_image.id, 
                      'item_id': item_image.item.id,
                      'src': os.path.join(settings.MEDIA_URL,item_image.image.name,)
                      }
            status = 200
        else:
            result = {'fields': form.errors}
            status = 409
        return HttpResponse(simplejson.dumps(result), 
                            status=status, 
                            mimetype='application/json')

class DeleteItemImageView(AdminTemplateView):
    params = {}
    
    def post(self, request, id, *args, **kwargs):
        try:
            item_image = ItemImage.objects.get(id=id)
        except Item.DoesNotExist:
            raise Http404()
        id = item_image.item_id
        item_image.delete()
        return HttpResponseRedirect(reverse('edit_item', args=(id,)))
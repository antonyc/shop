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
from orders.models import Delivery, delivery_types, status_choices
from django import forms
from administration.views import AdminListView, AdminTemplateView

class ListDeliveriesView(AdminListView):
    template_name = 'catalog/delivery/list.html'
    model = Delivery
    queryset = Delivery.objects.all().order_by('-created_at')
    paginate_by = 50
    allow_empty = True

class EditForm(forms.Form):
    name = fields.CharField(max_length=255, required=False, label=ugettext("Name"))
    description = fields.CharField(max_length=255, required=True, label=ugettext('Description'))
    type = fields.ChoiceField(choices=delivery_types, required=True, label=ugettext("Type"))
    price = fields.FloatField(required=True, initial=0, label=ugettext("Price"))

class EditDeliveryView(AdminTemplateView):
    template_name = 'catalog/delivery/edit.html'

    def dispatch(self, *args, **kwargs):
        delivery_id = kwargs.pop('id', None)
        if delivery_id is not None:
            try:
                self.delivery = Delivery.objects.get(id=delivery_id)
            except Delivery.DoesNotExist:
                raise Http404()
        else:
            self.delivery = Delivery()
        self.params['delivery'] = self.delivery
        return super(EditDeliveryView, self).dispatch(*args, **kwargs)

    def get(self, *args, **kwargs):
        form = EditForm(initial={'name': self.delivery.name,
                                 'description': self.delivery.description,
                                 'type': self.delivery.type,
                                 'price': self.delivery.price,
                                 })
        self.params['form'] = form
        return self.render_to_response(self.params)

    def post(self, *args, **kwargs):
        def get_address_text(post):
            result = {}
            fields = ['country', 'city', 'street', 'building', 'office', 'description']
            for field in fields:
                value = post.get('address_'+field)
                if value is not None:
                    if field in ('country', 'city'):
                        if isinstance(value, int):
                            value = int(value)
                    result[field] = value
            return result
        def get_address_point(post):
            result = {}
            if all('address_'+_ in post and post['address_'+_] for _ in ('lat', 'lon')):
                result = {'lat': float(post['address_lat']),
                          'lon': float(post['address_lon']),}
            return result
        initial={'name': self.delivery.name,
                 'description': self.delivery.description,
                 'type': self.delivery.type,
                 'price': self.delivery.price,
                 }
        form = EditForm(self.request.POST)
        if form.is_valid():
            self.delivery.name = form.cleaned_data.get('name')
            self.delivery.description = form.cleaned_data.get('description')
            self.delivery.type = form.cleaned_data.get('type')
            self.delivery.price = form.cleaned_data.get('price')
            self.delivery.save()
            text_address = get_address_text(self.request.POST)
            point_address = get_address_point(self.request.POST)
            print 'point',self.request.POST
            if text_address:
                address = self.delivery.dynamic_properties['address']
                address['text'] = address.get('text', {})
                address['text'].update(text_address)
                self.delivery.dynamic_properties['address'] = address
            if point_address:
                address = self.delivery.dynamic_properties['address']
                address['point'] = address.get('point', {})
                address['point'].update(point_address)
                self.delivery.dynamic_properties['address'] = address
            else:
                if self.delivery.dynamic_properties.has_point():
                    del self.delivery.dynamic_properties['address']['point']
            self.delivery.save()
            return HttpResponseRedirect(reverse('show_deliveries'))
        else:
            self.params['form'] = form
            return self.render_to_response(self.params)
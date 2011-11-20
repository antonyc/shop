# -*- coding: utf-8 -*-
'''
Created on 31.07.2011

@author: chapson
'''
from catalog.models import Item, Category
from django.utils.translation import ugettext, ugettext_lazy
from django.forms import Form, fields
from django.forms.widgets import Textarea
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template.defaulttags import url
from django.core.urlresolvers import reverse
from orders.models import Delivery, delivery_types, status_choices
from django import forms
from administration.views import AdminListView, AdminTemplateView
from utils.base_view import get_address_text
from utils.forms import AmadikaForm

class ListDeliveriesView(AdminListView):
    template_name = 'catalog/delivery/list.html'
    model = Delivery
    queryset = Delivery.objects.all().order_by('-created_at')
    paginate_by = 50
    allow_empty = True

class EditForm(AmadikaForm):
    name = fields.CharField(max_length=255, required=False, label=ugettext("Name"))
    description = fields.CharField(max_length=255, required=True, label=ugettext('Description'))
    type = fields.ChoiceField(choices=delivery_types, required=True, label=ugettext("Type"))
    price = fields.FloatField(required=True, initial=0, label=ugettext("Price"))

class AddressForm(AmadikaForm):
    country__text = fields.CharField(max_length=50, label=ugettext_lazy("Country"))
    country = fields.IntegerField(widget=fields.HiddenInput)
    city__text = fields.CharField(max_length=50, label=ugettext_lazy("City"))
    city = fields.IntegerField(widget=fields.HiddenInput)
    street = fields.CharField(max_length=50, label=ugettext_lazy("Street"))
    building = fields.CharField(max_length=50, label=ugettext_lazy("Building"))
    office = fields.CharField(max_length=50, label=ugettext_lazy("Office"))
    description = fields.CharField(max_length=50, label=ugettext_lazy("How to find"))

class SingleItemView(AdminTemplateView):
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
        return super(SingleItemView, self).dispatch(*args, **kwargs)

class DeleteDeliveryView(SingleItemView):
    template_name = 'catalog/delivery/delete.html'

    def get(self, *args, **kwargs):
        return self.render_to_response(self.params)

    def post(self, *args, **kwargs):
        self.delivery.delete()
        return HttpResponseRedirect(reverse('show_deliveries'))

class EditDeliveryView(SingleItemView):
    template_name = 'catalog/delivery/edit.html'

    def get(self, *args, **kwargs):
        form = EditForm(initial={'name': self.delivery.name,
                                 'description': self.delivery.description,
                                 'type': self.delivery.type,
                                 'price': self.delivery.price,
                                 })
        self.params['form'] = form
        return self.render_to_response(self.params)

    def post(self, *args, **kwargs):
        def get_address_point(post):
            result = {}
            if all(post.get('address-'+_, False) for _ in ('lat', 'lon')):
                result = {'lat': float(post['address-lat']),
                          'lon': float(post['address-lon']),}
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
            if text_address:
                if self.delivery.dynamic_properties.has_address():
                    address = self.delivery.dynamic_properties['address']
                else:
                    address = {}
                address['text'] = address.get('text', {})
                address['text'].update(text_address)
                self.delivery.dynamic_properties['address'] = address
            if point_address:
                if self.delivery.dynamic_properties.has_address():
                    address = self.delivery.dynamic_properties['address']
                else:
                    address = {}
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
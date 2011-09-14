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

class AddressForm(forms.Form):
    country__text = fields.CharField(max_length=50, label=ugettext_lazy("Country"))
    country = fields.CharField(max_length=10, widget=fields.HiddenInput)
    city__text = fields.CharField(max_length=50, label=ugettext_lazy("City"))
    city = fields.CharField(max_length=10, widget=fields.HiddenInput)
    street = fields.CharField(max_length=50, label=ugettext_lazy("Street"))
    building = fields.CharField(max_length=50, label=ugettext_lazy("Building"))
    office = fields.CharField(max_length=50, label=ugettext_lazy("Office"))
    description = fields.CharField(max_length=50, label=ugettext_lazy("Description"))

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
            fields = ['country', 'city', 'street', 'city__text', 'country__text', 'building', 'office', 'description']
            for field in fields:
                value = post.get('address-'+field)
                if value is not None:
                    if field in ('country', 'city'):
                        if isinstance(value, int):
                            value = int(value)
                    result[field] = value
            if not result.get('city__text') and result.get('city'):
                result['city'] = ''
            if not result.get('country__text') and result.get('country'):
                result['country'] = ''
            return result
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
#            print 'addre',self.delivery.dynamic_properties['address'], text_address
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
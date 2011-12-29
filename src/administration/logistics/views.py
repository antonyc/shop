'''
Created on 31.07.2011

@author: chapson
'''
from django.conf import settings
from django.utils.translation import ugettext
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from business_events.models import Event
from orders.models import Order, OrderItem, STATUSES, DELETED
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.forms.models import ModelForm
from django.utils import simplejson
from administration.views import AdminTemplateView
from utils.forms import AmadikaModelForm


class ListOrdersView(AdminTemplateView):
    template_name = 'catalog/order_list.html'
    params = {}
    paginate_by = 50
    def get(self, request, *args, **kwargs):
        self.params = {}
        qs = Order.objects.all().order_by('-created_at')
        if qs.count() <= self.paginate_by:
            self.params['is_paginated'] = False
            self.params['object_list'] = qs
        else:
            self.params['is_paginated'] = True
            paginator = Paginator(qs, self.paginate_by)
            try:
                page = self.request.GET.get('page', 1)
                objects = paginator.page(page)
            except (EmptyPage, InvalidPage):
                objects = paginator.page(paginator.num_pages)
            self.params['paginator'] = objects
            self.params['object_list'] = objects.object_list
        return self.render_to_response(self.params)


class EditOrderView(AdminTemplateView):
    template_name = 'catalog/order_edit.html'
    def get(self, request, id, *args, **kwargs): 
        params = {}
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            raise Http404()
        params['order'] = order
        params['delete_status'] = DELETED
        statuses = dict(STATUSES)
        del statuses[order.status]
        if DELETED in statuses:
            del statuses[DELETED]
        status_keys = statuses.keys()
        status_keys.sort()
        params['statuses'] = []
        for key in status_keys:
            params['statuses'].append((key, statuses[key]))
        return self.render_to_response(params)


class OrderItemForm(AmadikaModelForm):
    class Meta:
        model = OrderItem
        fields = ('quantity',)


class EditOrderItemView(AdminTemplateView):
    def post(self, request, id, *args, **kwargs):
        try:
            order_item = OrderItem.objects.get(id=id)
        except OrderItem.DoesNotExist:
            raise Http404()
        else:
            previous = {'quantity': order_item.quantity}
        form = OrderItemForm(request.POST, 
                             instance=order_item)
        if form.is_valid():
            order_item = form.save()
            event = Event(user=request.user,
                          notify=True)
            event.save()
            event.dynamic_properties['event'] = {'type': Event.EVENT_TYPES.order_item_change,
                                                 'status': {'was': previous['quantity'],
                                                            'now': order_item.quantity},
                                                 'order_id': order_item.order.id,}
            if not self.request.is_ajax:
                return HttpResponseRedirect(reverse('edit_order', kwargs={'id': order_item.order.id}))
            result = {'id': order_item.id, 
                      'quantity': order_item.quantity,}
            status = 200
        else:
            if not self.request.is_ajax:
                return HttpResponse(status=500)
            result = {'fields': form.errors}
            status = 409
        return HttpResponse(simplejson.dumps(result), 
                            status=status, 
                            mimetype='application/json')

    
class DeleteOrderItemView(AdminTemplateView):
    def post(self, request, id, *args, **kwargs):
        try:
            order_item = OrderItem.objects.get(id=id)
        except OrderItem.DoesNotExist:
            raise Http404()
        id = order_item.item_id
        event = Event(user=request.user,
                      notify=True)
        event.save()
        event.dynamic_properties['event'] = {'type': 'order_item_delete',
                                             'status': {'was': order_item.quantity},
                                             'order_id': order_item.order.id,}
        order_item.delete()
        if not self.request.is_ajax:
            return HttpResponseRedirect(reverse('edit_order', args=[id])) 
        return HttpResponse(simplejson.dumps([]), 
                            status=200, 
                            mimetype='application/json')


class StatusOrderView(AdminTemplateView):
    def post(self, request, id, *args, **kwargs):
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            raise Http404()
        status = int(request.POST['status'])
        if not status in dict(STATUSES):
            return HttpResponse(status=403)
        previous_status = order.status
        order.status = status
        order.save()
        event = Event(user=request.user,
                      notify=True)
        event.save()
        event.dynamic_properties['event'] = {'type': 'order_status_changed',
                                             'status': {'was': previous_status,
                                                        'now': status},
                                             'order_id': order.id,}
        if not self.request.is_ajax:
            return HttpResponseRedirect(reverse('edit_order', args=[order.id])) 
        return HttpResponse(simplejson.dumps([]), 
                            status=200, 
                            mimetype='application/json')

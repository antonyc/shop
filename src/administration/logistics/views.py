'''
Created on 31.07.2011

@author: chapson
'''
from django.conf import settings
from django.utils.translation import ugettext
from django.core.paginator import Paginator
from orders.models import Order, OrderItem, STATUSES, DELETED
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.forms.models import ModelForm
from django.utils import simplejson
from administration.views import AdminTemplateView

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
            self.params['object_list'] = Paginator(qs, self.paginate_by)
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
        return self.render_to_response(params)

class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ('quantity',)
    
class EditOrderItemView(AdminTemplateView):
    def is_ajax(self, request):
        return 'X-Requested-With' in request.META and request.META['X-Requested-With'] == 'XMLHttpRequest'

    def post(self, request, id, *args, **kwargs):
        try:
            order_item = OrderItem.objects.get(id=id)
        except OrderItem.DoesNotExist:
            raise Http404()
        form = OrderItemForm(request.POST, 
                             instance=order_item)
        if form.is_valid():
            order_item = form.save()
            if not self.is_ajax(request):
                return HttpResponseRedirect(reverse('edit_order_item', args=[order_item.item_id])) 
            result = {'id': order_item.id, 
                      'quantity': order_item.quantity,}
            status = 200
        else:
            result = {'fields': form.errors}
            status = 409
        return HttpResponse(simplejson.dumps(result), 
                            status=status, 
                            mimetype='application/json')
        
class DeleteOrderItemView(AdminTemplateView):
    def is_ajax(self, request):
        return 'X-Requested-With' in request.META and request.META['X-Requested-With'] == 'XMLHttpRequest'

    def post(self, request, id, *args, **kwargs):
        try:
            order_item = OrderItem.objects.get(id=id)
        except OrderItem.DoesNotExist:
            raise Http404()
        id = order_item.item_id
        order_item.delete()
        if not self.is_ajax(request):
            return HttpResponseRedirect(reverse('edit_order', args=[id])) 
        return HttpResponse(simplejson.dumps([]), 
                            status=200, 
                            mimetype='application/json')

class StatusOrderView(AdminTemplateView):
    def is_ajax(self, request):
        return 'X-Requested-With' in request.META and request.META['X-Requested-With'] == 'XMLHttpRequest'

    def post(self, request, id, *args, **kwargs):
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            raise Http404()
        status = int(request.POST['status'])
        if not status in dict(STATUSES):
            return HttpResponse(status=403)
        order.status = status
        order.save()
        if not self.is_ajax(request):
            return HttpResponseRedirect(reverse('edit_order', args=[order.id])) 
        return HttpResponse(simplejson.dumps([]), 
                            status=200, 
                            mimetype='application/json')

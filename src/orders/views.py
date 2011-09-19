# Create your views here.
from django import forms
from django.http import HttpResponse, Http404
from django.utils import simplejson
from django.utils.translation import ugettext_lazy
from orders.models import Delivery, DeliveryTypes, Order, OrderComment
from utils.base_view import BaseTemplateView
from utils.strings import parse_markup

class OrderView(BaseTemplateView):
    def dispatch(self, *args, **kwargs):
        request = args[0]
        id = kwargs.pop('id')
        try:
            self.obj = Order.public_objects.select_related(depth=2).get(id=id)
        except Order.DoesNotExist:
            raise Http404
        if request.user != self.obj.user:
            return HttpResponse(status=403)
        return super(OrderView, self).dispatch(*args, **kwargs)


class AddCommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea, label=ugettext_lazy('comment text'), required=True)


class ShowOrderView(OrderView):
    template_name = 'orders/show.html'
    def get(self, *args, **kwargs):
        self.params['order'] = self.obj
        self.params['comments'] = self.obj.ordercomment_set.all()
        self.params['comment_form'] = AddCommentForm()
        return self.render_to_response(self.params)

class CommentOrderView(OrderView):
    def post(self, *args, **kwargs):
        form = AddCommentForm(self.request.POST)
        if form.is_valid():
            OrderComment(user=self.request.user,
                         order=self.obj,
                         body=parse_markup(form.cleaned_data.get('body').replace("\r\n", "\n").strip(), strip_title=True)).save()
        return self.redirect_to_referrer()

class DeliveryView(BaseTemplateView):
    """
    Get the closest delivery point (e.g. customer pickup) from the given point
    """
    def get(self, *args, **kwargs):
        lon = float(self.request.GET.get('lon'))
        lat = float(self.request.GET.get('lat'))
        delivery_maps = {}
        for delivery in Delivery.public_objects.filter(type=DeliveryTypes.shopper):
            if delivery.dynamic_properties.has_point():
                point = delivery.dynamic_properties['address']['point']
                distance_square = (point['lat']-lat)*(point['lat']-lat)+(point['lon']-lon)*(point['lon']-lon)
                delivery_maps[distance_square] = delivery
        result = {}
        if delivery_maps:
            keys = delivery_maps.keys()
            keys.sort()
            result = {'id': delivery_maps[keys[0]].id}
        return HttpResponse(simplejson.dumps(result), mimetype='application/json')


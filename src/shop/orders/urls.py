from orders.views import DeliveryView, ShowOrderView, CommentOrderView
from views import OrderView
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'(?P<id>\d+)/$', ShowOrderView.as_view(), name='view_order'),
    url(r'(?P<id>\d+)/comment/$', CommentOrderView.as_view(), name='add_comment'),
    url(r'nearest_delivery/$', DeliveryView.as_view(), name="nearest_delivery"),
)


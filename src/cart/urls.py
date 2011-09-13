from django.conf.urls.defaults import *
from users.views import LoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt
from cart.views import CartQuantityView, ShowCartView

urlpatterns = patterns('',
    url(r'item/(?P<url>[\w\-]+)/quantity/$', CartQuantityView.as_view(), name="cart_item_quantity"),
    url(r'cart/$', ShowCartView.as_view(), name='cart_show')
)
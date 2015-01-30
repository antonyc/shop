from django.conf.urls.defaults import *
from loginza.decorators import login_required
from users.views import LoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt
from cart.views import CartQuantityView, ShowCartView

urlpatterns = patterns('',
    url(r'item/(?P<url>[\w\-]+)/quantity/$', CartQuantityView.as_view(), name="cart_item_quantity"),
    url(r'$', login_required(ShowCartView.as_view()), name='cart_show')
)
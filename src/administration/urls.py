from django.conf.urls.defaults import *
from administration.deliveries.views import ListDeliveriesView, EditDeliveryView, DeleteDeliveryView
from administration.items.views import ListItemsView, EditItemsView,\
    DeleteItemsView
from administration.categories.views import ListCategoriesView, EditCategoryView,\
    DeleteCategoryView
from administration.images.views import UploadItemImageView, DeleteItemImageView
from administration.logistics.views import ListOrdersView, EditOrderItemView,\
    EditOrderView, StatusOrderView, DeleteOrderItemView
from administration.admin_pages.views import EditPageView, ListPagesView
from administration.site_configuration.views import ShowSettingsView, ParseMenuText

urlpatterns = patterns('',
    url(r'items/$', ListItemsView.as_view(), name='list_items'),
    url(r'items/(?P<id>\d+)/edit/$', EditItemsView.as_view(), name='edit_item'),
    url(r'items/add/$', EditItemsView.as_view(), name='add_item'),
    url(r'items/(?P<id>\d+)/delete/$', DeleteItemsView.as_view(), name='delete_item'),
    url(r'categories/$', ListCategoriesView.as_view(), name='list_categories'),
    url(r'categories/(?P<id>\d+)/edit/$', EditCategoryView.as_view(), name='edit_category'),
    url(r'categories/add/$', EditCategoryView.as_view(), name='add_category'),
    url(r'categories/(?P<id>\d+)/delete/$', DeleteCategoryView.as_view(), name='delete_category'),    
    url(r'items/(?P<id>\d+)/images/add/$', UploadItemImageView.as_view(), name='upload_item_image'),
    url(r'images/(?P<id>\d+)/delete/$', DeleteItemImageView.as_view(), name='delete_item_image'),
    url(r'orders/$', ListOrdersView.as_view(), name='list_orders'),
    url(r'orders/(?P<id>\d+)/edit/$', EditOrderView.as_view(), name='edit_order'),
    url(r'orders/item/(?P<id>\d+)/edit/$', EditOrderItemView.as_view(), name='edit_order_item'),
    url(r'orders/item/(?P<id>\d+)/delete/$', DeleteOrderItemView.as_view(), name='delete_order_item'),
    url(r'orders/(?P<id>\d+)/status/$', StatusOrderView.as_view(), name='order_status'),
    url(r'pages/add/$', EditPageView.as_view(), name='add_page'),
    url(r'pages/(?P<id>\d+)/edit/$', EditPageView.as_view(), name='edit_page'),
    url(r'pages/$', ListPagesView.as_view(), name='list_pages'),
    url(r'deliveries/(?P<id>\d+)/delete/$', DeleteDeliveryView.as_view(), name='delete_delivery'),
    url(r'deliveries/(?P<id>\d+)/edit/$', EditDeliveryView.as_view(), name='edit_delivery'),
    url(r'deliveries/add/$', EditDeliveryView.as_view(), name='add_delivery'),
    url(r'deliveries/$', ListDeliveriesView.as_view(), name='show_deliveries'),
    url(r'settings/$', ShowSettingsView.as_view(), name='show_settings'),
    url(r'interactive_parser/$', ParseMenuText.as_view(), name='interactive_parser'),
    url(r'users/', include('administration.users.urls')),
    url(r'$', ListPagesView.as_view()),
)

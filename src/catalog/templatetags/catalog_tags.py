from django.core.urlresolvers import reverse

__author__ = 'chapson'

from django.conf import settings
from catalog.models import Item, ItemImage
from catalog.models import gen_thumbnail
from django.utils import translation
from django.utils.translation import ugettext
from geocoding.models import Geomodel
from utils import policy
from orders.models import get_address
from utils.templatetags.util_tags import class_block
from administration.deliveries.views import AddressForm
from django import template
register = template.Library()


@register.simple_tag
def get_item_main_image(item):
    return image_thumbnail(Item.public_objects.main_image(item), 'small')

@register.simple_tag
def image_thumbnail(image, width=None, height=None):
    if not isinstance(image, ItemImage):
        return
    if height is None:
        size = settings.THUMBNAILS.get(width)
        if size is not None:
            width, height = size
    if width is None:
        width = settings.THUMBNAIL_SIZE.width
    if height is None:
        height = settings.THUMBNAIL_SIZE.height
    return gen_thumbnail(image.image, (width, height))

@register.simple_tag
def get_quantity(item, q_map):
    return q_map.get(item.id, 0)

@register.simple_tag
def category_url(category):
    cats = list(category.get_ancestors())
    cats.append(category)
    url_parts = map(lambda cat: cat.url, cats)
    return reverse('show_category', kwargs={'url': '/'.join(url_parts)})
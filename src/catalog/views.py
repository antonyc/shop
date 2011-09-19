# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.urlresolvers import reverse
from django.http import Http404
from catalog.models import Item, Category
from django.conf import settings
from utils.base_view import BaseTemplateView, set_cart

class ItemView(BaseTemplateView):
    def dispatch(self, *args, **kwargs):
        url = kwargs.pop('url')
        try:
            self.obj = Item.public_objects.get(url=url)
        except Item.DoesNotExist:
            raise Http404
        return super(ItemView, self).dispatch(*args, **kwargs)

class ShowItemView(ItemView):
    template_name = 'catalog/item.html'
    def get(self, request, *args, **kwargs):
        main_image = Item.public_objects.main_image(self.obj)
        self.params['main_image'] = main_image
        if main_image:
            self.params['other_images'] = self.obj.itemimage_set.exclude(id=main_image.id)
        self.params['item'] = self.obj
        cart = set_cart(self.request.session)
        quantity = 0
        for item in cart['items']:
            if item['id'] == self.obj.id and item['quantity'] > 0:
                quantity = item['quantity']
        self.params['quantity'] = quantity
        return self.render_to_response(self.params)

class ShowCategoryView(BaseTemplateView):
    template_name = 'category/show.html'
    paginate_by = 20
    def get(self, request, *args, **kwargs):
        url = kwargs.pop('url', None)
        parents = Category.objects.filter(parent=None)
        if url is not None:
            split = url.split('/')
            category = None
            crumbs = []
            url = []
            for category_url in split:
                try:
                    category = Category.objects.get(url=category_url, parent=category)
                    url.append(category.url)
                    crumbs.append({'url': reverse('show_category', kwargs={'url': "/".join(url)}),
                                   'text': category.name})
                except Category.DoesNotExist:
                    raise Http404
            self.params['breadcrumbs'] = crumbs
            items = category.all_items
        else:
            items = set()
            for cat in parents:
                items.update(cat.all_items)
            items.update(Item.objects.filter(categories=None))
        cart = set_cart(self.request.session)
        self.params['parent_categories'] = parents
        self.params['cart_quantities'] = dict(map(lambda item: (item['id'], item['quantity']), cart['items']))
        if len(items) <= self.paginate_by:
            self.params['is_paginated'] = False
            self.params['object_list'] = items
        else:
            self.params['is_paginated'] = True
            paginator = Paginator(items, 20)
            try:
                page = self.request.GET.get('page', 1)
                objects = paginator.page(page)
            except (EmptyPage, InvalidPage):
                objects = paginator.page(paginator.num_pages)
            self.params['paginator'] = objects
            self.params['object_list'] = objects.object_list
        return self.render_to_response(self.params)
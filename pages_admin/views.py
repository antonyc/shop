# coding: utf-8

from pretend import stub
from django.views import generic
from django.core.urlresolvers import reverse

from .forms.create import CreateForm, UpdateForm
from pages_core.models import Page


class CreatePage(generic.CreateView):
    model = Page
    template_name = 'pages_admin/page_form.html'
    form_class = CreateForm

    def get_success_url(self, *args, **kwargs):
        return reverse('admin:page_list')


class ListPages(generic.ListView):
    model = Page
    template_name = 'pages_admin/page_list.html'

    def get_context_data(self, **kwargs):
        context = super(ListPages, self).get_context_data(**kwargs)
        context['bootstrap_page'] = stub(
            paginator=context['paginator'])
        return context


class UpdatePage(generic.UpdateView):
    model = Page
    template_name = 'pages_admin/page_form.html'
    form_class = UpdateForm

    def get_success_url(self, *args, **kwargs):
        return reverse('admin:page_list')


class DeletePage(generic.DeleteView):
    model = Page
    template_name = 'pages_admin/page_confirm_delete.html'

    def get_success_url(self):
        return reverse('admin:page_list')

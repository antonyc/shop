# coding: utf-8

from django import forms

from pages_core.logic import create_page, update_page
from pages_core.models import Page


class CreateForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('title', 'body')

    def save(self, commit=True):
        return create_page(
            title=self.cleaned_data['title'],
            body=self.cleaned_data['body']
        )


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('title', 'body')

    def save(self, commit=True):
        return update_page(
            page=self.instance,
            title=self.cleaned_data['title'],
            body=self.cleaned_data['body']
        )

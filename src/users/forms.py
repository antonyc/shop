# -*- coding:utf-8 -*-

import re
from django import forms
from django.contrib.auth.models import User
from django.forms.util import ErrorDict
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext


phone_number_cleaner = re.compile(r'[^\d]')


class CompleteReg(forms.Form):
#    username = forms.CharField(max_length=255, min_length=3)
    email = forms.EmailField(max_length=255, min_length=5)
    phone_number = forms.CharField(max_length=20, min_length=4)
    
    def __init__(self, user_id, *args, **kwargs):
        self.user_id = user_id
#        self.user = User.objects.select_related(depth=1).get(id=user_id)
        super(CompleteReg, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        emails = User.objects.filter(email=email).exclude(id=self.user_id).count()
        if emails > 0:
            raise ValidationError(ugettext('username with such email (%s) already exists') % email)
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number', '')
        return re.sub(phone_number_cleaner, '', phone_number)
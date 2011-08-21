# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.forms.util import ErrorDict
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext

class CompleteReg(forms.Form):
#    username = forms.CharField(max_length=255, min_length=3)
    email = forms.EmailField(max_length=255, min_length=5)
    
    def __init__(self, user_id, *args, **kwargs):
        self.user_id = user_id
#        self.user = User.objects.select_related(depth=1).get(id=user_id)
        super(CompleteReg, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
#        usernames = User.objects.filter(username=email).exclude(id=self.user_id).count()
#        if usernames > 0:
#            raise ValidationError(ugettext('username with such username (%s) already exists') % email)
        emails = User.objects.filter(email=email).exclude(id=self.user_id).count()
        if emails > 0:
            raise ValidationError(ugettext('username with such email (%s) already exists') % email)
        return email
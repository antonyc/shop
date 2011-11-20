'''
Created on 31.07.2011

@author: chapson
'''
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils.translation import ugettext_lazy
from administration.views import AdminListView, AdminTemplateView
from django.contrib.auth.models import User, AnonymousUser
from users.models import has_orders, orders
from utils.forms import AmadikaForm


class ListUsers(AdminListView):
    template_name = 'admin/users/list.html'
    params = {}
    paginate_by = 50
    queryset = User.objects.all().order_by('-is_active', 'is_staff')


class UserView(AdminTemplateView):
    def dispatch(self, request, id=None, *args, **kwargs):
        try:
            user = User.objects.select_related(depth=1).get(id=id)
#            print 'view for user', user
        except User.DoesNotExist:
            if id is not None:
                raise Http404()
            else:
                user = User()
        self.obj = user
        self.params['obj'] = user
        return super(UserView, self).dispatch(request, id, *args, **kwargs)


class ShowUser(UserView):
    template_name = 'admin/users/show.html'
    def get(self, request, *args, **kwargs):
        self.params['orders'] = orders(self.obj)
        self.params['has_orders'] = has_orders(self.obj)
        return self.render_to_response(self.params)

no_yes_choices = ((0, ugettext_lazy("No", )),
                  (1, ugettext_lazy("Yes")))


def unique_field_validator(field_name, model, skip=None):
    def unique_user_validator(value):
#        print User.objects.all(), skip
        value = value.strip()
        if skip == value:
            return
        try:
            model.objects.get(**{field_name: value})
            error_message = "User with %(field_name)s \"%(value)s\" already exists" % {
                'field_name': field_name,
                'value': value}
            raise ValidationError(error_message)
        except User.DoesNotExist:
            pass
    return unique_user_validator


class EditForm(AmadikaForm):
    username = forms.CharField(max_length=255, label=ugettext_lazy("Username (Login)"), required=True)
    email = forms.EmailField(max_length=255, required=True, label=ugettext_lazy("User email"))
    first_name = forms.CharField(max_length=255, label=ugettext_lazy("First name"))
    last_name = forms.CharField(max_length=255, label=ugettext_lazy("Last name"))
    ui_lang = forms.CharField(max_length=2, min_length=2, label=ugettext_lazy("Interface language"))
    is_staff = forms.ChoiceField(choices=no_yes_choices, label=ugettext_lazy("Is staff"), required=False, initial=0)
    is_superuser = forms.ChoiceField(choices=no_yes_choices, label=ugettext_lazy("Is superuser"), required=False, initial=0)

    def __init__(self, user, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.obj = user

    def clean(self):
        cleaned_data = super(EditForm, self).clean()
#        print self.__dict__
        username = cleaned_data.get('username', '').strip()
        email = cleaned_data.get('email', '').strip()
        unique_field_validator('username', User, self.obj.username)(username)
        unique_field_validator('email', User, self.obj.email)(email)
        return self.cleaned_data


class EditUser(UserView):
    template_name = 'admin/users/edit.html'

    def get_form(self, request, user):
        data = None
        if request.method == 'POST':
            data = request.POST
        initial = {'email': user.email,
                   'is_staff': user.is_staff,
                   'is_superuser': user.is_superuser,
                   'username': user.username}
        try:
            profile = user.get_profile()
        except:
            pass
        else:
            initial.update({'first_name': profile.res_first_name,
                            'last_name': profile.res_last_name,
                            'ui_lang': profile.ui_lang})
        form = EditForm(user=user,
                        initial=initial,
                        data=data)
        return form

    def get(self, request, *args, **kwargs):
        self.params['form'] = self.get_form(request, self.obj)
        return self.render_to_response(self.params)

    def post(self, request, *args, **kwargs):
        form = self.get_form(request, self.obj)
        if form.is_valid():
            self.obj.email = form.cleaned_data.get('email').strip()
            self.obj.username = form.cleaned_data.get('username').strip()
            self.obj.save()
            profile = self.obj.get_profile()
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.ui_lang = form.cleaned_data.get('ui_lang')
            profile.save()
            return HttpResponseRedirect(reverse('show_user', kwargs={'id': self.obj.id}))
        else:
            self.params['form'] = form
            return self.render_to_response(self.params)

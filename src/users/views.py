# -*- coding:utf-8 -*-
import urllib2, logging, traceback
import hashlib, datetime
from django.utils import simplejson
from django.conf import settings
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext
from utils.strings import translit
from django.contrib.auth import login
from django.contrib.auth.models import User
from users.models import UserProfile
from urllib2 import quote

from users import forms
from django import http
from django.contrib import messages, auth
from django.shortcuts import redirect, render_to_response
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from loginza import signals, models
from loginza.templatetags.loginza_widget import _return_path
from django.contrib.auth.views import logout

#loginza routines

def loginza_auth_handler(sender, user, identity, **kwargs):
    try:
        # it's enough to have single identity verified to treat user as verified
        models.UserMap.objects.get(user=user, verified=True)
        auth.login(sender, user)
    except models.UserMap.DoesNotExist:
        sender.session['users_complete_reg_id'] = identity.id
        return redirect(reverse('users.views.complete_registration'))

signals.authenticated.connect(loginza_auth_handler)

def complete_registration(request):
    def generate_username(json_data):
        data = simplejson.loads(json_data)
        name = data.get('name')
        first_name = ''
        family_name = ''
        if name:
            first_name = name.get('first_name')
            family_name = name.get('last_name')
        username = data.get('nickname')
        if not username and name:
            username = ' '.join((first_name, family_name))
        username = translit(username or u'user')
        nickname = username
        cnt = 1
        while True:
            try:
                User.objects.get(username=nickname)
                nickname = '%s_%s' % (username, cnt)
                cnt += 1
            except User.DoesNotExist:
                return nickname
    if request.user.is_authenticated():
        return http.HttpResponseForbidden(u'Вы попали сюда по ошибке')
    try:
        identity_id = request.session.get('users_complete_reg_id', None)
        user_map = models.UserMap.objects.select_related('user','identity').get(identity__id=identity_id, verified=False)
    except models.UserMap.DoesNotExist:
        return http.HttpResponseForbidden(u'Вы попали сюда по ошибке')
    if request.method == 'POST':
        form = forms.CompleteReg(user_map.user.id, request.POST)
        if form.is_valid():
            user_map.user.username = generate_username(user_map.identity.data)
            user_map.user.email = form.cleaned_data['email']
            user_map.user.save()

            user_map.verified = True
            user_map.save()

            user = auth.authenticate(user_map=user_map)
            auth.login(request, user)

            messages.info(request, u'Добро пожаловать!')
#            del request.session['users_complete_reg_id']
            return redirect(_return_path(request))
    else:
        form = forms.CompleteReg(user_map.user.id, initial={
            'email': user_map.user.email,
            })
    return render_to_response('accounts/complete_registration.html',
                              {'form': form},
                              context_instance=RequestContext(request),
                              )


class LoginView(TemplateView):
    template_name = 'accounts/user_login.html'
    def get(self, request, *args, **kwargs):
        params = {'host_name': settings.HOST_NAME,
                  'request': request}
        path = request.GET.get('next', None)
        if path is not None and path not in settings.LOGINZA_AMNESIA_PATHS:
            request.session['loginza_return_path'] = path
#        next = request.GET.get('next', None)
#        if next is not None:
#            params['next'] = '?next='+next
        return self.render_to_response(params)
    
    def post(self, request, *args, **kwargs):
        request.session['loginza_token'] = request.POST['token']
        params = {'host_name': settings.HOST_NAME,
                  'get_data': True,
                  'request': request,}
        return self.render_to_response(params)

class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        next = request.GET.get('next', '/')
        return HttpResponseRedirect(next)
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
from django.contrib.auth import login, authenticate
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
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail.message import EmailMessage

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
    def generate_username(data):
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
    def generate_password(user):
        return hashlib.md5(user.username + user.email + str(datetime.datetime.now())).hexdigest()[:7]

    def send_email(user, password):
        message = EmailMessage(subject=ugettext("Registration complete"),
                               body=ugettext("You can login with \"%(username)s\" and password: %(password)s") % 
                                {'username': user.username,
                                 'password': password,},
                               to=(user.email,),
                               from_email=settings.SERVER_EMAIL,)
        message.send(True)
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
            data = simplejson.loads(user_map.identity.data)
            
            user_map.user.username = generate_username(data)
            user_map.user.email = form.cleaned_data['email']
            password = generate_password(user_map.user)
            user_map.user.set_password(password)
            user_map.user.save()
            
            send_email(user_map.user, password)
            
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
        params['authentication_form'] = AuthenticationForm()
        params['show_login_window'] = 'loginza'
        return self.render_to_response(params)
    
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['username'],
                         password=form.cleaned_data['password'])
            auth.login(request, user)
        params = {'host_name': settings.HOST_NAME,
                  'request': request}
        params['authentication_form'] = form
        params['show_login_window'] = 'straight'
        return self.render_to_response(params)
#        request.session['loginza_token'] = request.POST['token']
#        params = {'host_name': settings.HOST_NAME,
#                  'get_data': True,
#                  'request': request,}
#        return self.render_to_response(params)

class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        next = request.GET.get('next', '/')
        return HttpResponseRedirect(next)
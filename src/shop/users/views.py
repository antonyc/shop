# -*- coding:utf-8 -*-
from django.template.loader import render_to_string
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
from business_events.models import Event
from utils import email_name
from utils.base_view import BaseTemplateView
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
            except User.DoesNotExist:
                return nickname
            else:
                nickname = '%s_%s' % (username, cnt)
                cnt += 1
                
    def generate_password(user):
        return hashlib.md5(user.username + user.email + str(datetime.datetime.now())).hexdigest()[:7]

    def send_email(user, password):
        return
        message = EmailMessage(subject=ugettext("Registration complete"),
                               body=ugettext("You can login with \"%(username)s\" and password: %(password)s") % 
                                {'username': user.username,
                                 'password': password,},
                               to=(user.email,),
                               from_email=settings.SERVER_EMAIL,)
        message.send(True)
    if request.user.is_authenticated():
        return http.HttpResponseForbidden(ugettext("You got here by mistake"))
    try:
        identity_id = request.session.get('users_complete_reg_id', None)
        user_map = models.UserMap.objects.select_related('user','identity').get(identity__id=identity_id, verified=False)
    except models.UserMap.DoesNotExist:
        return http.HttpResponseForbidden(ugettext("You got here by mistake"))
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
            user.first_name = user.get_profile().res_first_name
            user.last_name = user.get_profile().res_last_name
            user.save()

            profile = user.get_profile()
            profile.phone_number = form.cleaned_data['phone_number']
            profile.save()

            event = Event(user=user,
                          notify=True)
            event.save()
            event.dynamic_properties['event'] = {'type': 'new_user',
                                                 'username': user.username,
                                                 'user_id': user.id}
            params = {'password': password,
                      'user': user,
                      'site_url': "http://%s/" % settings.HOST_NAME,
                      'hostname': settings.HOST_NAME}
            body = render_to_string('accounts/email/registration_complete.html', params)
            message = EmailMessage(from_email=settings.SERVER_EMAIL,
                         to=(user.email,),
                         body=body)
            message.content_subtype = 'html'
            message.send()
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


class LoginView(BaseTemplateView):
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

class LogoutView(BaseTemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        next = request.GET.get('next', '/')
        return HttpResponseRedirect(next)
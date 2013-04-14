# coding=utf-8
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import datetime
from base.forms import LoginForm
from base.base_view import BaseView


class LoginView(BaseView):
    def get(self, request,*args, **kwargs):
        loginForm = LoginForm()
        c = RequestContext(request, {'form':loginForm})
        c.update(csrf(request))
        tt = loader.get_template('base_login.html')
        return HttpResponse(tt.render(c))
    
    def post(self, request,*args, **kwargs):
        loginForm=LoginForm(request.POST)
        if loginForm.is_valid():
             username = loginForm.cleaned_data['username']
             password = loginForm.cleaned_data['password']
             remember = loginForm.cleaned_data['remember']
             user = authenticate(username=username, password=password)
             if user is not None:
                if user.is_active:  # 登录成功
                    login(request,user)
                    c = {'result':'success'}
                else:
                    c={'login_failed':'true'}
             else:
                c={'login_failed':'true'}
        else:
             c=loginForm.errors
        return self._get_json_respones(c)
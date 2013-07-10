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
    def get(self, request, version='',*args, **kwargs):
        if version=='m':
            return self.getm(request)
        loginForm = LoginForm()
        c = RequestContext(request, {'form':loginForm})
        c.update(csrf(request))
        tt = loader.get_template(version+'base_login.html')
        return HttpResponse(tt.render(c))

    def getm(self,request):
         tid=request.GET.get('tid')
         rid=request.GET.get('rid')

         if tid != None:
            if rid is None:
                refer='/m/topic/'+tid+'/1'
            else:
                refer='/m/topic/'+tid+'/reply/'+rid
         else:
            refer='/m/my/bookmarks/1'

         if request.user.is_active:
             return HttpResponseRedirect(refer)
         c = RequestContext(request, {'refer':refer})
         c.update(csrf(request))
         tt = loader.get_template('mbase_login.html')
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
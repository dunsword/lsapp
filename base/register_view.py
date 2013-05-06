# coding=utf-8

from django.views.generic.base import View
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
import os
from django.template import RequestContext
from base.models import User, UserFollow
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import datetime
from ls.models import Feed, Document, Category, Topic, TopicReply
from ls.topic_forms import TopicForm, TopicReplyForm, TopicService, TopicReplyService
from ls.document_forms import DocumentService
from django.utils.decorators import method_decorator
from base.base_view import BaseView, PageInfo
from base.forms import RegisterUserForm


class RegisterView(BaseView):
    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
        c = RequestContext(request, {'form':form})
        c.update(csrf(request))
        tt = loader.get_template('register.html')
        return HttpResponse(tt.render(c))
    
    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repassword = form.cleaned_data['repassword']
            email = form.cleaned_data['email']              
            
            try:
                # check paramters
                user = User.objects.create_user(username, email, password)
                user.is_staff = False
                user.save()
                loginUser=authenticate(username=username, password=password)
                login(request, loginUser)        
                return self._get_json_respones({'result':'success'})
            except Exception, e:
                return self._get_json_respones({'result':'failed','exception':e})
        else:
            c = RequestContext(request, {'form':form})
            return self._get_json_respones({'result':'failed','errors':form.errors})
           

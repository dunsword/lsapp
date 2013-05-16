# coding=utf-8
from django.views.generic.base import View
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
import os
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import datetime
from ls.models import Feed,Document,Category,Topic,TopicReply
from ls.topic_forms import TopicForm,TopicReplyForm,TopicService,TopicReplyService,DocumentForm
from ls.document_forms import DocumentService
from django.utils.decorators import method_decorator
from base.base_view import BaseView, PageInfo
from base.models import User
from base.forms import UserForm
class UserEditView(BaseView):
    def get(self,request, userid,*args, **kwargs):
        user=request.user
        if not user.is_staff:
            return HttpResponseRedirect("/404")
        euser=User.objects.get(pk=userid)
        userForm=UserForm(instance=euser)
        c= RequestContext(request,{"userForm":userForm})
        tt = loader.get_template('base_user_edit.html')
        return HttpResponse(tt.render(c))
    
    def post(self,request, userid,*args, **kwargs):
        user=request.user
        if not user.is_staff:
            return self._get_json_respones({'result':'error'})
        
        euser=User.objects.get(pk=userid)
        former_password=euser.password
        
        password=request.POST['password']
        change_password=True
        if password==None or password==u'':
            data=request.POST.copy()
            data['password']=former_password
            change_password=False
        else:
            data=request.POST
            
        userForm=UserForm(data=data,instance=euser)
        
            
        if userForm.is_valid():
            euser2=userForm.save(commit=False)
            if change_password:
                euser2.set_password(userForm.cleaned_data['password'])
            else:
                euser2.password=former_password
            euser2.save()
            return self._get_json_respones({'result':'success'})
        else:
            return self._get_json_respones({'result':'failed',
                                        'errors':userForm.errors})
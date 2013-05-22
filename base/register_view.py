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
from base.mail.mail import SentMail
from base.email_bind_models import EmailBindRecord

class EmailBindView(BaseView):
     @method_decorator(login_required)
     def get(self, request, *args, **kwargs):
          #user=request.user
        c = RequestContext(request, {})
        tt = loader.get_template('base_email_bind.html')

        return HttpResponse(tt.render(c))

     @method_decorator(login_required)
     def post(self,request,*args,**kwargs):
        user=request.user
        email=request.POST['email']

        records=EmailBindRecord.objects.filter(userid__exact=user.id).order_by('-created_at')[0:5]

        bind=EmailBindRecord.objects.createEmailBindRecord(user.id,email)


        url= 'http://weibols.sinaapp.com/email_active?code=%s&uid=%s'%(str(bind.active_code),str(bind.userid))
        content=u'''<h4>欢迎注册小说推荐网</h4>
         <p>请点击以下地址验证您的邮箱：
         <a href='%s'</a>%s</p>
         <p>如不能点击，请复制以上地址到浏览器地址栏。</p>
         <br/>
         <p>这是一封自动发送的邮件，请勿回复！  </p>
         <p>--小说推荐网</p>'''%(url,url)

        success=SentMail.sentMail(email,u'小说推荐网邮箱激活',content)
        if success:
            return self._get_json_respones({'result':'success'})
        else:
            return self._get_json_respones({'result':'failed'})

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
           

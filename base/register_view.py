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
from datetime import datetime, timedelta

class EmailActiveView(BaseView):
    def get(self,request,*args,**kwargs):
        code=request.GET['code']
        uid=int(request.GET['uid'])
        query=EmailBindRecord.objects.filter(userid__exact=uid).filter(is_used__exact=False).order_by('-created_at')[0:5]
        recs=list(query)
        if len(recs)>0:
            rec=recs[0]
            timeLimit=timedelta(hours=24)
            now=datetime.now()
            if now-rec.created_at>timeLimit:
                ctx={"result":False,"message":"验证码已经过期！"}
            elif rec.active_code==code:
                user=User.objects.get(pk=uid)
                user.email=rec.email
                user.email_bind=True
                user.save()

                rec.is_used=True
                rec.updated_at=now
                rec.save()
                ctx={"result":True,"message":"邮箱地址验证成功！"}
            else:
                ctx={"result":False,"message":"验证码不正确！"}
        else:
            ctx={"result":False,"message":"验证码不正确！"}

        c = RequestContext(request, ctx)
        tt = loader.get_template('base_email_active.html')

        return HttpResponse(tt.render(c))

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

        records=EmailBindRecord.objects.filter(userid__exact=user.id).filter(is_used__exact=False).order_by('-created_at')[0:5]
        rs=list(records)
        now=datetime.now()

        if len(rs)>0:



            oneMin=timedelta(minutes=1)
            if now-rs[0].created_at<oneMin:
                return self._get_json_respones({'result':'failed','message':u'请1分钟后再试！'})

        if len(rs)>=5:
            first=rs[len(rs)-1]
            oneHour=timedelta(hours=1)
            if now-first.created_at<oneHour:
                return self._get_json_respones({'result':'failed','message':u'发送次数过多，请1小时后再试！'})

        bind=EmailBindRecord.objects.createEmailBindRecord(user.id,email)
        host=request.get_host()
        url= 'http://%s/email_active?code=%s&uid=%s'%(host,str(bind.active_code),str(bind.userid))
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
           

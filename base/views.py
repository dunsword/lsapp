# coding=utf-8
from django.template import Context, loader
from django.http import HttpResponse,HttpResponseRedirect
import os
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.template import RequestContext
from django.contrib.auth.models import User
from base.forms import RegisterUserForm,LoginForm, SetupForm
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login,logout
from MySQLdb.connections import IntegrityError
from django.conf import settings
from django.contrib.auth.decorators import login_required

def do_login(request):
    if request.method=='POST':
        loginForm=LoginForm(request.POST)
        if loginForm.is_valid():
            username=loginForm.cleaned_data['username']
            password=loginForm.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_active: #登录成功
                    login(request,user)
                    return HttpResponseRedirect('/')
                else:
                    return __render_login(request, loginForm,msg="用户帐号被禁用！")
            else:
                return __render_login(request, loginForm,msg="用户名或密码错误！")
        else:
            return __render_login(request,loginForm)
    else:
        pass
    
    loginForm=LoginForm()
    return __render_login(request, loginForm)

def __render_login(request,loginForm,msg=None):
    c=RequestContext(request,{'form':loginForm,'msg':msg})
    c.update(csrf(request))
    tt = loader.get_template('login.html')
    return HttpResponse(tt.render(c))

def do_logout(request):
    logout(request)
    return HttpResponseRedirect("/login")

def register(request):
    if request.method=='POST':
        form= RegisterUserForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            repassword=form.cleaned_data['repassword']
            email=form.cleaned_data['email']              
                    
            try:
                #check paramters
                user=User.objects.create_user(username, email, password)
                user.is_staff=True
                user.save()
            except Exception, e:
                c=RequestContext(request,{'form':form,'exception':e})
                tt = loader.get_template('register.html')
                return HttpResponse(tt.render(c))
            return HttpResponseRedirect('regsuccess')
        else:
            c=RequestContext(request,{'form':form})
            tt = loader.get_template('register.html')
            return HttpResponse(tt.render(c))
    
    form= RegisterUserForm()
    c=RequestContext(request,{'form':form})
    c.update(csrf(request))
    tt = loader.get_template('register.html')
    return HttpResponse(tt.render(c))

def reg_success(request):
    c=RequestContext(request,{})
    tt = loader.get_template('regsuccess.html')
    return HttpResponse(tt.render(c))
    
def page_404(request):
    c=RequestContext(request,{})
    tt = None
    user=request.user
    if user==None:
        tt=loader.get_template('unlogin_404.html')
    else:
        tt=loader.get_template('login_404.html')
    return HttpResponse(tt.render(c))

def do_register(request):
    if request.method=='POST':
        form= RegisterUserForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            repassword=form.cleaned_data['repassword']
            email=form.cleaned_data['email']   
                                
            try:
                #check paramters
                user=User.objects.create_user(username, email, password)
                user.is_staff=True
                user.save()
            except Exception, e:
                c=RequestContext(request,{'form':form,'exception':e})
                tt = loader.get_template('register.html')
                return HttpResponse(tt.render(c))
            c=RequestContext(request,{'user',user})
            
            return HttpResponseRedirect('regsuccess')
           
        else:
            c=RequestContext(request,{'form':form})
            tt = loader.get_template('register.html')
            return HttpResponse(tt.render(c))
    return HttpResponseRedirect('login')

@login_required
def setup(request):
    form=None
    if request.method=='POST':
        form= SetupForm(request.POST,request.FILES)
        user=request.user
        if form.is_valid():
            avatarTempFile=request.FILES['avatar']
            handleFile(user.id,avatarTempFile)
            firstName=form.cleaned_data['firstName']
            lastName=form.cleaned_data['lastName']
            user.first_name=firstName
            user.last_name=lastName
            user.save()
    else: 
        form=SetupForm()
    c=RequestContext(request,{'form':form})
    tt = loader.get_template('setup.html')
    return HttpResponse(tt.render(c))

def handleFile(uid,f):
    fileName=settings.STATIC_ROOT+'/avatar/'+str(uid)+'.jpg'
    destination=open(fileName,'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
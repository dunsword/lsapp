# coding=utf-8
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
import os
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.template import RequestContext
from base.models import User
from base.forms import RegisterUserForm, LoginForm, SetupForm, SetpassForm, SetAvatarForm
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from MySQLdb.connections import IntegrityError
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json
from PIL import Image

def do_login(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:  # 登录成功
                    login(request, user)
                    return HttpResponseRedirect('/setup')
                else:
                    return __render_login(request, loginForm, msg="用户帐号被禁用！")
            else:
                return __render_login(request, loginForm, msg="用户名或密码错误！")
        else:
            return __render_login(request, loginForm)
    else:
        pass
    
    loginForm = LoginForm()
    return __render_login(request, loginForm)

def __render_login(request, loginForm, msg=None):
    c = RequestContext(request, {'form':loginForm, 'msg':msg})
    c.update(csrf(request))
    tt = loader.get_template('login.html')
    return HttpResponse(tt.render(c))

def do_logout(request):
    logout(request)
    return HttpResponseRedirect("/login")

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repassword = form.cleaned_data['repassword']
            email = form.cleaned_data['email']              
                    
            try:
                # check paramters
                user = User.objects.create_user(username, email, password)
                user.is_staff = True
                user.save()
            except Exception, e:
                c = RequestContext(request, {'form':form, 'exception':e})
                tt = loader.get_template('register.html')
                return HttpResponse(tt.render(c))
            return HttpResponseRedirect('regsuccess')
        else:
            c = RequestContext(request, {'form':form})
            tt = loader.get_template('register.html')
            return HttpResponse(tt.render(c))
    
    form = RegisterUserForm()
    c = RequestContext(request, {'form':form})
    c.update(csrf(request))
    tt = loader.get_template('register.html')
    return HttpResponse(tt.render(c))

def reg_success(request):
    c = RequestContext(request, {})
    tt = loader.get_template('regsuccess.html')
    return HttpResponse(tt.render(c))
    
def page_404(request):
    c = RequestContext(request, {})
    tt = None
    user = request.user
    if user == None:
        tt = loader.get_template('unlogin_404.html')
    else:
        tt = loader.get_template('login_404.html')
    return HttpResponse(tt.render(c))

def do_register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repassword = form.cleaned_data['repassword']
            email = form.cleaned_data['email']   
                                
            try:
                # check paramters
                user = User.objects.create_user(username, email, password)
                user.is_staff = True
                user.save()
            except Exception, e:
                c = RequestContext(request, {'form':form, 'exception':e})
                tt = loader.get_template('register.html')
                return HttpResponse(tt.render(c))
            c = RequestContext(request, {'user', user})
            
            return HttpResponseRedirect('regsuccess')
           
        else:
            c = RequestContext(request, {'form':form})
            tt = loader.get_template('register.html')
            return HttpResponse(tt.render(c))
    return HttpResponseRedirect('login')

@login_required
def setup(request):
    form = None
    if request.method == 'POST':
        form = SetupForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            # avatarTempFile=request.FILES['avatar']
            # handleFile(user.id,avatarTempFile)
            user.first_name = form.cleaned_data['firstName']
            # user.last_name=form.cleaned_data['lastName']
            user.nickname = form.cleaned_data['nickname']
            
            user.save()
    else:  # GET
        user = request.user
        data = {
              'firstName':user.first_name,
              'nickname':user.nickname,
              }
        form = SetupForm(data)
    c = RequestContext(request, {'form':form})
    tt = loader.get_template('setup.html')
    return HttpResponse(tt.render(c))

@login_required
def setpass(request):
    form = None
    if request.method == 'POST':
        form = SetpassForm(request.POST)
        user = request.user
        if form.is_valid():
            password = form.cleaned_data['password']
            authUser = authenticate(username=user.username, password=password)
            if authUser is not None:
                newPassword = form.cleaned_data['newPassword']
                user.set_password(newPassword)
                user.save()
            else:
                errors = form.errors['password'] = u'密码错误！'
    else:  # GET
        user = request.user
        
        form = SetpassForm()
    c = RequestContext(request, {'form':form})
    tt = loader.get_template('setpass.html')
    return HttpResponse(tt.render(c))

@login_required
def setAvatar(request):
    form = SetAvatarForm()
    if request.method == 'POST':
        form = SetAvatarForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            avatarTempFile = request.FILES['avatar']
            handleFile(user.id, avatarTempFile)
            
    c = RequestContext(request, {'form':form, 'head_template_file':'setavatar_head.html'})
    tt = loader.get_template('setavatar.html')
    return HttpResponse(tt.render(c))

def __jsonRespones(ctx, **httpresponse_kwargs):
    content= json.dumps(ctx);
    return HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

@login_required
def cropAvatar(request):
    avatarWidth = int(request.POST['avatar_width'])
    avatarHeight = int(request.POST['avatar_height'])
    avatarMarginLeft = int(request.POST['avatar_marginLeft'])
    avatarMarginTop = int(request.POST['avatar_marginTop'])
    avatarRealWidth = int(request.POST['avatar_real_x'])
    avatarRealHeight = int(request.POST['avatar_real_y'])
    
    
    user = request.user
    fileName = settings.STATIC_ROOT + '/avatar/' + str(user.id) + '.jpg'
    img=Image.open(fileName)
    img.thumbnail((avatarRealWidth,avatarRealHeight),Image.ANTIALIAS)
    avatar=img.crop((avatarMarginLeft,avatarMarginTop,avatarMarginLeft+avatarWidth,avatarMarginTop+avatarHeight))
    avatar.thumbnail((60,60),Image.ANTIALIAS)
    avatar.save(settings.STATIC_ROOT + '/avatar/' + str(user.id) + '_avatar_60_60.jpg',"JPEG",quality=100)
    result={'width':avatarWidth,'height':avatarHeight,'left':avatarMarginLeft,'top':avatarMarginTop,'real_width':avatarRealWidth,'real_height':avatarRealHeight , 'result':'success',}
    return __jsonRespones(result);

def handleFile(uid, f):
    fileName = settings.STATIC_ROOT + '/avatar/' + str(uid) + '.jpg'
    destination = open(fileName, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

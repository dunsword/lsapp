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

@login_required
def users(request):
    c=RequestContext(request,{})
    c.update(csrf(request))
    tt = loader.get_template('admin.html')
    return HttpResponse(tt.render(c))
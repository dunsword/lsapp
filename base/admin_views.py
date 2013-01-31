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
from django.contrib.auth.decorators import permission_required

@login_required
@permission_required('base/admin_task',login_url="/404")
def users(request):
    users=User.objects.all()[:30]
    c=RequestContext(request,{'users':users})
    c.update(csrf(request))
    tt = loader.get_template('admin_users.html')
    return HttpResponse(tt.render(c))
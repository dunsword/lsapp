# coding=utf-8
from django.template import Context, loader
from django.http import HttpResponse,HttpResponseRedirect
import os
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.template import RequestContext
from django.contrib.auth.models import User
from base.admin_forms import UserEditForm
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login,logout
from MySQLdb.connections import IntegrityError
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from base.messages import GLOBAL_MESSAGES

@login_required
@permission_required('base/admin_task',login_url="/404")
def index(request):
    c=RequestContext(request,{ })
    c.update(csrf(request))
    tt = loader.get_template('admin.html')
    return HttpResponse(tt.render(c))


@login_required
@permission_required('base/admin_task',login_url="/404")
def user_list(request):
    users=User.objects.all()[:30]
    c=RequestContext(request,{'users':users})
    c.update(csrf(request))
    tt = loader.get_template('admin_users.html')
    return HttpResponse(tt.render(c))

@login_required
@permission_required('base/admin_task',login_url="/404")
def user_edit(request,user_id):
    if request.method=='GET':
        msg=request.GET.get('msg')
        
        user=User.objects.get(pk=user_id)
        ctx=__user_2form(request,user,None)
        tt = loader.get_template('admin_user_edit.html')
        return HttpResponse(tt.render(ctx))
    elif request.method=='POST':
        user=User.objects.get(pk=user_id)
        userForm=UserEditForm(request.POST)
        if userForm.is_valid():
            user.email=userForm.cleaned_data['email']
            user.first_name=userForm.cleaned_data['first_name']
            user.last_name=userForm.cleaned_data['last_name']
            user.save()
            msg="SAVE_SUCCESS"
        else:
            msg="SAVE_FAILED"
        ctx=__user_2form(request,user,msg)
        tt = loader.get_template('p_admin_user_edit_form.html')
        return HttpResponse(tt.render(ctx))
        #return HttpResponseRedirect('/admin/user/edit/'+str(user.id)+'?msg=SAVE_SUCCESS');
    pass

def __user_2form(request,user,msg):
    data={
              'username':user.username,
              'email':user.email,
              'first_name':user.first_name,
              'last_name':user.last_name
              }
    userForm=UserEditForm(data)
    c=RequestContext(request,{'user':user,'form':userForm,'msg':msg})
    c.update(csrf(request))
    return c
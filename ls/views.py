# coding = utf-8
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
import os
from django.template import RequestContext
from base.models import User
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json
from datetime import datetime
from ls.models import Category

def index(request):
      feeds=Feed.objects.all()[0:20]
      c = RequestContext(request, {'feeds':feeds})
    
      tt = loader.get_template('ls_index.html')
      return HttpResponse(tt.render(c))


from base.base_view import BaseView


class LsView(BaseView):
    def __init__(self, **kwargs):
        super(LsView,self).__init__(**kwargs)
    
    def getContext(self,request,ctx={}):
        category=Category.objects.get(pk=2)
        cats=Category.objects.getCategory(2)
        c= RequestContext(request,{"category":category,"categorylist":cats})
        c.update(ctx)
        return c
        
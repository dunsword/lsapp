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
from ls.models import Feed

def index(request):
      feeds=Feed.objects.all()[0:20]
      c = RequestContext(request, {'feeds':feeds})
    
      tt = loader.get_template('ls_index.html')
      return HttpResponse(tt.render(c))


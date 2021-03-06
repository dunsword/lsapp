# coding=utf-8

from django.views.generic.base import View
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect

from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import datetime
from ls.models import Feed,Document,Category,Topic,TopicReply
from ls.topic_forms import TopicForm,TopicReplyForm,TopicService,TopicReplyService
from ls.document_forms import DocumentService
from django.utils.decorators import method_decorator
from ls.views import LsView
from base.models import User
from django.db.models import Q

class SearchView(LsView):
     def get(self,request,keyword,*args, **kwargs):
         
         topics=Topic.objects.filter(Q(title__contains=keyword))[0:30]
         result_count=topics.count()
         c=self.getContext(request, {'keyword':keyword,'topics':topics})
         tt = loader.get_template('ls_search.html')
         return HttpResponse(tt.render(c))
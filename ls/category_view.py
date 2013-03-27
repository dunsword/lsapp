# coding=utf-8
'''
Created on 2013-3-27
@author: XPS
'''
from django.views.generic.base import View
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
import os
from django.template import RequestContext
from base.models import User,UserFollow
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import datetime
from ls.models import Feed,Document,Category,Topic,TopicReply
from ls.topic_forms import TopicForm,TopicReplyForm,TopicService,TopicReplyService
from ls.document_forms import DocumentService
from django.utils.decorators import method_decorator
from base.base_view import BaseView, PageInfo

class CategoryView(BaseView):
    def __init__(self):
        self.docSrv=DocumentService()
        
    def get(self,request, categoryid, page=1,*args, **kwargs):
        categoryid=int(categoryid)
        page=int(page)
        category=Category.objects.get(pk=categoryid)
        topics=Topic.objects.filter(categoryid__exact=categoryid)
        count=topics.count()
        pageInfo=PageInfo(page,count,10)
        
        docs=self.docSrv.getHotDocuments(categoryid)
        c = RequestContext(request, {'category':category,'topics':topics,'pageInfo':pageInfo,'hot_docs':docs})
        tt = loader.get_template('ls_category.html')
        return HttpResponse(tt.render(c))
# coding=utf-8
__author__ = 'paul'

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
from base.base_view import BaseView,PageInfo
from bookmark_models import BookMark


class MBookmarkView(BaseView):
    def get(self,request,page,*args, **kwargs):
        user=request.user
        uid=user.id
        page=int(page)

        count=BookMark.objects.filter(uid__exact=uid).count()
        pageInfo=PageInfo(page=page,itemCount=count,pageSize=10,baseUrl='/m/my/bookmarks/')
        bms=BookMark.objects.filter(uid__exact=uid).order_by('-updated_at')[pageInfo.startNum:pageInfo.endNum]
        c = RequestContext(request,{'bookmarks':bms,'pageInfo':pageInfo})
        tt = loader.get_template('mls_bookmarks.html')
        return HttpResponse(tt.render(c))




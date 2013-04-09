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

class CategoryNewTopicView(BaseView):
    @method_decorator(login_required)
    def post(self,request,*args, **kwargs):
        topicTitle=request.POST['topic_title']
        topicContent=request.POST['topic_content']
        catId=request.POST['cat_id']
        user=request.user
        topic=Topic.objects.create_topic(user, topicTitle, topicContent, catId)
        return self._get_json_respones({"success":"true","topic_id":topic.id,"topic_title":topicTitle,"topic_content":topicContent})
    
    def get(self,request,*args, **kwargs):
        topicid=request.GET['topic_id']
        topic=Topic.objects.get(pk=topicid)
        c = RequestContext(request, {'topic':topic})
        tt = loader.get_template('ls_category_topic_item.html')
        return HttpResponse(tt.render(c))
        
class CategoryView(BaseView):
    def __init__(self):
        self.docSrv=DocumentService()
        
    def get(self,request, categoryid, page=1,*args, **kwargs):
        #prepare parameters
        categoryid=int(categoryid)
        page=int(page)
        
        #TODO should be deferent page for top level cat and leaf level cat
        category=Category.objects.get(pk=categoryid)
        if category.level==1:
            topics=Topic.objects.filter(catid_parent__exact=categoryid).order_by('-created_at')
            cats=Category.objects.getCategory(category.id)
        else:
            cats=Category.objects.getCategory(category.parent_id)
            topics=Topic.objects.filter(categoryid__exact=categoryid).order_by('-created_at')
        count=topics.count()
        pageInfo=PageInfo(page,count,10)
        
        docs=self.docSrv.getHotDocuments(categoryid)
        c = RequestContext(request, {'category':category,'topics':topics,'pageInfo':pageInfo,'hot_docs':docs,'categorylist':cats})
        tt = loader.get_template('ls_category.html')
        return HttpResponse(tt.render(c))
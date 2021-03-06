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
from base.models import User
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from ls.models import Feed,Document,Category,Topic,TopicReply
from ls.topic_forms import TopicForm,TopicReplyForm,TopicService,TopicReplyService
from ls.document_forms import DocumentService
from django.utils.decorators import method_decorator
from base.base_view import BaseView, PageInfo
from ls.views import LsView
from base.storage.client import AvatarClient
from django.db.models import Q

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
        
class CategoryView(LsView):
    def __init__(self):
        self.docSrv=DocumentService()
        
    def get(self,request, categoryid, page=1,*args, **kwargs):
        #prepare parameters
        categoryid=int(categoryid)
        page=int(page)
        
        #默认是显示正常状态的帖子，为管理需要，可以通过指定状态显示（TODO：以后要加权限判断）
        if 'status' not in request.GET:
            status=1
        else:
            status=request.GET['status']
        
        cats=None
        #TODO should be deferent page for top level cat and leaf level cat
        category=Category.objects.get(pk=categoryid)
        if category.level==1:
            topic_count=Topic.objects.filter(catid_parent__exact=categoryid).count()
            pageInfo=PageInfo(page,topic_count,30,'/cat/'+str(category.id)+'/')
            topics=Topic.objects.filter(catid_parent__exact=categoryid).filter(status__exact=status).order_by('-created_at')[pageInfo.startNum:pageInfo.endNum]
   
        else:
            topic_count=Topic.objects.filter(categoryid__exact=categoryid).count()
            pageInfo=PageInfo(page,topic_count,30)
            cats=Category.objects.getCategory(category.parent_id) 
            topics=Topic.objects.filter(Q(categoryid__exact=categoryid)|Q(catid1__exact=categoryid)|Q(catid2__exact=categoryid)).filter(status__exact=status).order_by('-created_at')[pageInfo.startNum:pageInfo.endNum]
       
      
        c = self.getContext(request,{'category':category,'topics':topics,'pageInfo':pageInfo})
        if cats:
            c.update({'categorylist':cats})
        tt = loader.get_template('ls_category.html')
        return HttpResponse(tt.render(c))
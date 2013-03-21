# coding=utf-8
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
from django.utils.decorators import method_decorator

class TopicView(View):
    
    #@method_decorator(login_required)
    def get(self,request, topicid,page=1,*args, **kwargs):
        topicService=TopicService()
        trSrv=TopicReplyService()
        topic=Topic.objects.get(pk=topicid)
        replyList=trSrv.getTopicReplyList(topic.id, page)
        topicForm=topicService.getTopicForm(1)
        topicForm.is_valid()
        c = RequestContext(request, {'topic':topicForm,'reply_list':replyList})
        tt = loader.get_template('ls_topic.html')
        return HttpResponse(tt.render(c))
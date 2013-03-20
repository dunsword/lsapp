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
from ls.topic_forms import TopicForm,TopicReplyForm
from django.utils.decorators import method_decorator

class TopicView(View):
    
    #@method_decorator(login_required)
    def get(self,request, *args, **kwargs):
        topic=Topic.objects.get(pk=1)
        topicForm=TopicForm(instance=topic)
        topicForm.is_valid()
        c = RequestContext(request, {'topic':topicForm})
        tt = loader.get_template('ls_topic.html')
        return HttpResponse(tt.render(c))
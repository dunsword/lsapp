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
from ls.models import Feed, Document, Category, Topic, TopicReply
from ls.topic_forms import TopicForm, TopicReplyForm, TopicService, TopicReplyService
from ls.document_forms import DocumentService
from django.utils.decorators import method_decorator
from base.base_view import BaseView, PageInfo
from base.models import User

class MyTopicView(BaseView):
    def __init__(self):
        self.docSrv = DocumentService()
        
    def get(self, request, userid, page=1, *args, **kwargs):
        cats = Category.objects.getCategory(2)
        docs = self.docSrv.getHotDocuments(2)
         
        user = User.objects.get(pk=userid)
        topics = Topic.objects.filter(userid__exact=userid).order_by('-created_at')
        topic_count = Topic.objects.filter(userid__exact=userid).count()
        pageInfo = PageInfo(page, topic_count, 30, '/cat/' + str(userid) + '/')
        c = RequestContext(request, {'topics':topics, 'pageInfo':pageInfo, 'cuser':user, 'categorylist':cats, 'hot_docs':docs})
        tt = loader.get_template('ls_user_home.html')
        return HttpResponse(tt.render(c))

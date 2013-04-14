# coding=utf-8
from django.views.generic.base import View
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
import os
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
from base.base_view import BaseView, PageInfo


class BaseTopicView(BaseView):
    def __init__(self, **kwargs):
        super(BaseTopicView,self).__init__(**kwargs)
        self.tSrv=TopicService()
        self.trSrv=TopicReplyService()
        self.docSrv=DocumentService()
        
class TopicView(BaseTopicView):
    
    #@method_decorator(login_required)
    def get(self,request, topicid,page=1,*args, **kwargs):
        topicid=int(topicid)
        page=int(page)
        topic=Topic.objects.get(pk=topicid)
        
        replyList=self.tSrv.getTopicReplyList(topic.id, page)
        topicForm=self.tSrv.getTopicForm(topic)
        topicForm.is_valid()
        docs=self.docSrv.getHotDocuments(topicForm.instance.categoryid)
        
        #标签推荐
        cats=Category.objects.getCategory(2)
        pageInfo=PageInfo(page,topic.reply_count,self.tSrv.PAGE_SIZE)
        replyForm=TopicReplyForm()
        c = RequestContext(request, {'topic':topicForm,'reply_list':replyList,'hot_docs':docs,"replyForm":replyForm,"pageInfo":pageInfo,"categorylist":cats})
        tt = loader.get_template('ls_topic.html')
        return HttpResponse(tt.render(c))
    
    def to_document(self,request, topic, page):
        doc=topic.getDocument()
        replyList=self.tSrv.getTopicReplyList(topic.id, page)
        topicForm=self.tSrv.getTopicForm(topic)
        topicForm.is_valid()
        docs=self.docSrv.getHotDocuments(topicForm.instance.categoryid)
        
        pageInfo=PageInfo(page,topic.reply_count,self.tSrv.PAGE_SIZE)
        
        replyForm=TopicReplyForm()
        c = RequestContext(request, {'topic':topicForm,'doc':doc,'reply_list':replyList,'hot_docs':docs,"replyForm":replyForm,"pageInfo":pageInfo})
        tt = loader.get_template('ls_topic_document.html')
        return HttpResponse(tt.render(c))
    
class TopicReplyView(BaseTopicView):
    @method_decorator(login_required)
    def post(self,request,topicid,*args,**kwargs):
        rc=request.POST['replyContent']
        user=request.user
        replyForm=TopicReplyForm({'userid':user.id,'username':user.username,'topicid':topicid,'content':rc,'title':'','created_at':datetime.now(),'updated_at':datetime.now(),'status':1})
        if(replyForm.is_valid()):
            self.tSrv.addReply(replyForm)
            ctx ={'success':'true','replyid':replyForm.instance.id,'time':replyForm.cleaned_data['created_at'].strftime('%H:%M'),'content':replyForm.cleaned_data['content']}
        else:
            ctx={'success':'false','errors':replyForm.errors}
        return self._get_json_respones(ctx)
    
    def get(self,request,replyid,*args,**kwargs):
        topicReply=TopicReply.objects.get(pk=replyid)
        c = RequestContext(request,{'reply':topicReply})
        tt = loader.get_template('ls_topic_reply_item.html')
        return HttpResponse(tt.render(c))
        
        
        
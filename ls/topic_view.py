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
from ls.document_forms import DocumentService
from django.utils.decorators import method_decorator
from django.utils import simplejson as json



class PageInfo(object): 
    class PageItem(object):
        def __init__(self,page,isCurrent):
            self.page=page
            self.isCurrent=isCurrent
        
    def __init__(self,page,pageCount):
        self.page=page
        self.pageCount=pageCount
        self.items=self.getRange()
        
        #判断是否显示下一页
        if page<pageCount:
            self.next=page+1
        else:
            self.next=None
        
        #判断是否显示上一页
        if page>1:
            self.previous=page-1
        else:
            self.previous=None
        
        #判断是否显示第一页和最后一页
        self.first=None
        self.last=None
        small=page
        big=page
        for item in self.items:
            if small>item.page:
                small=item.page
            if big<item.page:
                big=item.page
        if small>1:
            self.first=1
        if big<self.pageCount:
            self.last=self.pageCount
        
    def getRange(self):
        start=self.getStart()
        end=start+4
        if end > self.pageCount:
            diff=end-self.pageCount
            end=self.pageCount
            start=start-diff
            if start<1:
                start=1
        return [PageInfo.PageItem(p,p==self.page) for p in range(start,end+1)]
        
    def getStart(self):
        start=self.page-2
        if start<1:
            start=1
        return start
        
class BaseView(View):
    def _get_json_respones(self,ctx, **httpresponse_kwargs):
        content= json.dumps(ctx);
        return HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)
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
        topicForm=self.tSrv.getTopicForm(1)
        topicForm.is_valid()
        docs=self.docSrv.getHotDocuments(topicForm.instance.categoryid)
        
        pageCount=self.tSrv.getPageCount(topic)
        
        pageInfo=PageInfo(page,pageCount)
        
        replyForm=TopicReplyForm()
        c = RequestContext(request, {'topic':topicForm,'reply_list':replyList,'hot_docs':docs,"replyForm":replyForm,"pageInfo":pageInfo})
        tt = loader.get_template('ls_topic.html')
        return HttpResponse(tt.render(c))
    
    
    
class TopicReplyView(BaseTopicView):
    @method_decorator(login_required)
    def post(self,request,topicid,*args,**kwargs):
        rc=request.POST['replyContent']
        user=request.user
        replyForm=TopicReplyForm({'userid':user.id,'username':user.username,'topicid':topicid,'content':rc,'title':'','created_at':datetime.now(),'updated_at':datetime.now(),'status':1})
        if(replyForm.is_valid()):
            self.tSrv.addReply(replyForm)
            ctx ={'success':'true','time':replyForm.cleaned_data['created_at'].strftime('%H:%M'),'content':replyForm.cleaned_data['content']}
        else:
            ctx={'success':'false','errors':replyForm.errors}
        return self._get_json_respones(ctx)
    
        
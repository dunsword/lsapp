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

class TopicView(View):
    def __init__(self, **kwargs):
        super(TopicView,self).__init__(**kwargs)
        self.tSrv=TopicService()
        self.trSrv=TopicReplyService()
        self.docSrv=DocumentService()
        
    #@method_decorator(login_required)
    def get(self,request, topicid,page=1,*args, **kwargs):
        topic=Topic.objects.get(pk=topicid)
        replyList=self.trSrv.getTopicReplyList(topic.id, page)
        topicForm=self.tSrv.getTopicForm(1)
        topicForm.is_valid()
        docs=self.docSrv.getHotDocuments(topicForm.instance.categoryid)
        
        replyForm=TopicReplyForm()
        c = RequestContext(request, {'topic':topicForm,'reply_list':replyList,'hot_docs':docs,"replyForm":replyForm})
        tt = loader.get_template('ls_topic.html')
        return HttpResponse(tt.render(c))
    
    def _get_json_respones(self,ctx, **httpresponse_kwargs):
        content= json.dumps(ctx);
        return HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)
    
class TopicReplyView(TopicView):
    @method_decorator(login_required)
    def post(self,request,topicid,*args,**kwargs):
        rc=request.POST['replyContent']
        user=request.user
        replyForm=TopicReplyForm({'userid':user.id,'username':user.username,'topicid':topicid,'content':rc})
        if(replyForm.is_valid()):
            replyForm.save()
            ctx ={'success':'true'}
        else:
            ctx={'success':'false','errors':replyForm.errors}
        return self._get_json_respones(ctx)
    
        
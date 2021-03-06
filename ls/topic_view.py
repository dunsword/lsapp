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
from ls.topic_forms import TopicForm,TopicReplyForm,TopicService,TopicReplyService,DocumentForm
from ls.document_forms import DocumentService
from django.utils.decorators import method_decorator
from base.base_view import BaseView, PageInfo
from ls.views import LsView
from sync.sync_page import syncThread
from sync.models import source_author
import re

class BaseTopicView(LsView):
    def __init__(self, **kwargs):
        super(BaseTopicView,self).__init__(**kwargs)
        self.tSrv=TopicService()
        self.trSrv=TopicReplyService()
        self.docSrv=DocumentService()

class ProxyView(BaseTopicView):
    def get(self,request,tid,page=1,*args, **kwargs):
        try:
            doc = Document.objects.get_by_source(19,tid)
        except Document.DoesNotExist:
            doc = syncThread(tid) #TODO           异步同步回复
        if doc==None:
             return HttpResponseRedirect('http://www.19lou.com/forum-26-thread-%s-1-1.html'%(str(tid)))
        else:
             return HttpResponseRedirect('/m/topic/'+str(doc.topic.id)+'/1')





PATTEN_REPLACE_19URL=re.compile('(?<=http://www.19lou.com/forum-26-thread-)\d+(?=-1-1.html)')
PATTEN_REPLACE_19URL_AUTHOR=re.compile('(?<=http://www.19lou.com/user/profile-)\d+(?=-1.html)')
PATTEN_REPLACE_19URL_AUTHOR_T=re.compile('(?<=http://www.19lou.com/user/thread-)\d+(?=-1.html)')
class TopicView(BaseTopicView):
    
    #@method_decorator(login_required)
    def get(self,request, topicid,version='',page=1,*args, **kwargs):
        topicid=int(topicid)
        page=int(page)
        topic=Topic.objects.get(pk=topicid)
        docForm=None
        chapters=None

        #获取章节
        if topic.isDocument:
            docForm=DocumentForm(instance=topic.getDocument(),prefix="doc")
            chapters=topic.getChapters()
            count=len(chapters)
            chapter_align=0 #用于补齐3个的数量
            if count%3>0:
                chapter_align=3-count%3
            for i in range(chapter_align):
                chapters.append({})
        content=topic.content

        #替换链接
        while True:
            m=PATTEN_REPLACE_19URL.search(content)
            if m==None:
                break
            tid_19=m.group()
            content=re.sub('http://www.19lou.com/forum-26-thread-%s-1-1.html'%(tid_19),
                       '&nbsp;<a href="http://mobile-proxy.weibols.com/proxy/%s">☞点击访问</a>&nbsp;'%(tid_19),content)

        while True:
            m=PATTEN_REPLACE_19URL_AUTHOR.search(content)
            if m==None:
                break
            uid19=m.group()
            user_link_name=u'☞点击访问'
            try:
                s_author=source_author.objects.get(uid__exact=uid19)
                user_link_name=u'☞'+s_author.username+u'帖子列表'
            except source_author.DoesNotExist:
                pass

            content=re.sub('http://www.19lou.com/user/profile-%s-1.html'%(uid19),
                        '&nbsp;<a href="/m/daren/%s">%s</a>&nbsp;'%(uid19,user_link_name),content)
        while True:
            m=PATTEN_REPLACE_19URL_AUTHOR_T.search(content)
            if m==None:
                break
            uid19=m.group()
            user_link_name=u'☞点击访问'
            try:
                s_author=source_author.objects.get(uid__exact=uid19)
                user_link_name=u'☞'+s_author.username+u'帖子列表'
            except source_author.DoesNotExist:
                pass

            content=re.sub('http://www.19lou.com/user/thread-%s-1.html'%(uid19),
                        '&nbsp;<a href="/m/daren/%s">%s</a>&nbsp;'%(uid19,user_link_name),content)

        replyList=self.tSrv.getTopicReplyList(topic.id, page)
        topicForm=TopicForm(instance=topic,prefix="topic")
        topicForm.is_valid()
        cat=topic.getCategory()

      
        #标签推荐
        
        pageInfo=PageInfo(page,topic.reply_count,self.tSrv.PAGE_SIZE)
        replyForm=TopicReplyForm()
        c = self.getContext(request,
                            {'page_title':topic.title,
                             'topic':topicForm,
                             'docForm':docForm,
                             'chapters':chapters,
                             'reply_list':replyList,
                             'category':cat,
                             "replyForm":replyForm,
                             "pageInfo":pageInfo,
                             'topic_content':content
                             })

        tt = loader.get_template(version+'ls_topic.html')
        return HttpResponse(tt.render(c))
    
    def post(self,request, topicid,*args, **kwargs):
        docForm=DocumentForm(data=request.POST,prefix="doc")
        topicForm=TopicForm(data=request.POST,prefix="topic")
        return self._get_json_respones({})

class TopicEditView(BaseTopicView):
    def get(self,request, topicid,*args, **kwargs):
        topic=Topic.objects.get(pk=topicid)
        docForm=None
        if topic.isDocument():
            docForm=DocumentForm(instance=topic.getDocument(),prefix="doc")
            topicForm=TopicForm(instance=topic,prefix="topic")
            c = RequestContext(request, {'topic':topicForm,'docForm':docForm})
            tt = loader.get_template('ls_topic_doc_edit.html')
        else:
            topicForm=TopicForm(instance=topic)
            c = RequestContext(request, {'topic':topicForm})
            tt = loader.get_template('ls_topic_edit.html')
        return HttpResponse(tt.render(c))
    
    @method_decorator(login_required)
    def post(self,request, topicid,*args, **kwargs):
        user=request.user
        if not user.is_staff:
            return self._get_json_respones({'result':'error'})
        
        topic=Topic.objects.get(pk=topicid)
        if topic.isDocument():
            doc=topic.getDocument()
        
            docForm=DocumentForm(data=request.POST,prefix="doc",instance=doc)
            topicForm=TopicForm(data=request.POST,prefix="topic",instance=topic)
        
            if topicForm.is_valid() and docForm.is_valid():
                topicForm.save()
                docForm.save()
                return self._get_json_respones({'result':'success'})
            else:
                return self._get_json_respones({'result':'failed',
                                        'topic_errors':topicForm.errors,
                                        'document_errors':docForm.errors})
        else:
            topicForm=TopicForm(data=request.POST,instance=topic) 
            if topicForm.is_valid():
                topicForm.save()
                return self._get_json_respones({'result':'success'})
            else:
                return self._get_json_respones({'result':'failed',
                                        'errors':topicForm.errors})




class TopicReplyView(BaseTopicView):
    @method_decorator(login_required)
    def post(self,request,topicid,*args,**kwargs):
        rc=request.POST['replyContent']
        user=request.user
        replyForm=TopicReplyForm({'userid':user.id,
                                  'username':user.username,
                                  'topicid':topicid,
                                  'content':rc,
                                  'title':'',
                                  'created_at':datetime.now(),
                                  'updated_at':datetime.now(),
                                  'source_url':'http://www.tuitui2.com',
                                  'source_pid':0,
                                  'status':1})
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


class TopicReplyEditView(BaseTopicView):
    def get(self,request,*args,**kwargs):
        tid=int(request.GET['tid'])
        rid=int(request.GET['rid'])
        topic=Topic.objects.get(pk=tid)
        reply=TopicReply.objects.get(pk=rid)
        form = TopicReplyForm(instance=reply)
        c = RequestContext(request,{'reply':reply,'topic':Topic,'form':form})
        tt = loader.get_template('ls_topic_reply_edit.html')
        return HttpResponse(tt.render(c))

    def post(self,request,*args,**kwargs):
        tid=int(request.POST['tid'])
        rid=int(request.POST['rid'])

        user=request.user
        if not user.is_staff:
            return self._get_json_respones({'result':'error'})

        reply=TopicReply.objects.get(pk=rid)
        replyForm=TopicReplyForm(data=request.POST,instance=reply)
        if replyForm.is_valid():
            replyForm.save()
            return self._get_json_respones({'result':'success'})
        else:
            return self._get_json_respones({'result':'failed',
                                            'errors':replyForm.errors})
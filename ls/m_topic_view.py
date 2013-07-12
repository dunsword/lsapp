# coding=utf-8
__author__ = 'paul'
from django.views.generic.base import View
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from ls.models import Document,Category,Topic,TopicReply
from ls.topic_forms import TopicForm,TopicReplyForm,TopicService,TopicReplyService,DocumentForm
from base.base_view import BaseView, PageInfo
from sync.models import source_author
from topic_view import BaseTopicView
from base.forms import LoginForm
from ls.bookmark_models import BookMark
import re
from django.db.models import Q
from datetime import datetime
from base.models import UserLoginLog

PATTEN_REPLACE_19URL=re.compile('(?<=http://www.19lou.com/forum-26-thread-)\d+(?=-1-1.html)')
PATTEN_REPLACE_19URL_AUTHOR=re.compile('(?<=http://www.19lou.com/user/profile-)\d+(?=-1.html)')
PATTEN_REPLACE_19URL_AUTHOR_T=re.compile('(?<=http://www.19lou.com/user/thread-)\d+(?=-1.html)')
class MTopicView(BaseTopicView):

    #@method_decorator(login_required)
    def get(self,request, topicid,page=1,*args, **kwargs):

        topicid=int(topicid)

        #如果是直接进入页面，有阅读记录就跳转到上次阅读的书签
        refer=request.META.get('HTTP_REFERER')
        if (refer is None or refer =='') and request.user.is_active:
            uid=request.user.id
            try:
                bookmark=BookMark.objects.filter(uid__exact=uid).get(tid=topicid)
                rid=bookmark.rid
                return HttpResponseRedirect('/m/topic/'+str(topicid)+"/reply/"+str(rid))
            except BookMark.DoesNotExist:
                pass #没有书签，继续


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
            content=re.sub('"http://www.19lou.com/forum-26-thread-%s-1-1.html"'%(tid_19),
                           '"/proxy/%s"'%(tid_19),content)
            content=re.sub('\'http://www.19lou.com/forum-26-thread-%s-1-1.html\''%(tid_19),
                           '"/proxy/%s"'%(tid_19),content)
            content=re.sub('>http://www.19lou.com/forum-26-thread-%s-1-1.html<'%(tid_19),
                           u'>☞点击访问<',content)
            content=re.sub('http://www.19lou.com/forum-26-thread-%s-1-1.html'%(tid_19),
                           u'<a href="/proxy/%s">☞点击访问</a>'%(tid_19),content)
                       #'&nbsp;<a href="http://mobile-proxy.weibols.com/proxy/%s">☞点击访问</a>&nbsp;'%(tid_19),content)

        comments=Comment.objects.filter(topicid__exact=topicid).filter(replyid__exact=0).order_by('-created_at')[0:5]

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

            content=re.sub(u'"http://www.19lou.com/user/profile-%s-1.html"'%(uid19),
                           u'"/m/daren/%s"'%(uid19),content)
            content=re.sub(u'\'http://www.19lou.com/user/profile-%s-1.html\''%(uid19),
                           u'"/m/daren/%s"'%(uid19),content)
            content=re.sub(u'>http://www.19lou.com/user/profile-%s-1.html<'%(uid19),
                           u'>☞点击访问<',content)
            content=re.sub(u'http://www.19lou.com/user/profile-%s-1.html'%(uid19),
                           u'<a href="/m/daren/%s">☞点击访问</a>'%(uid19),content)
                        #'&nbsp;<a href="/m/daren/%s">%s</a>&nbsp;'%(uid19,user_link_name),content)
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

            content=re.sub(u'"http://www.19lou.com/user/thread-%s-1.html"'%(uid19),
                           u'"/m/daren/%s"'%(uid19),content)
            content=re.sub(u'\'http://www.19lou.com/user/thread-%s-1.html\''%(uid19),
                           u'"/m/daren/%s"'%(uid19),content)
            content=re.sub(u'>http://www.19lou.com/user/thread-%s-1.html<'%(uid19),
                           u'>☞点击访问<',content)
            content=re.sub(u'http://www.19lou.com/user/thread-%s-1.html'%(uid19),
                           u'<a href="/m/daren/%s">☞点击访问</a>'%(uid19),content)
                        #'&nbsp;<a href="/m/daren/%s">%s</a>&nbsp;'%(uid19,user_link_name),content)


        topicForm=TopicForm(instance=topic,prefix="topic")
        topicForm.is_valid()
        cat=topic.getCategory()


        #标签推荐

        pageInfo=PageInfo(page,topic.reply_count,self.tSrv.PAGE_SIZE)

        c = self.getContext(request,
                            {'page_title':topic.title,
                             'topic':topicForm,
                             'docForm':docForm,
                             'chapters':chapters,
                             'category':cat,
                             "pageInfo":pageInfo,
                             'topic_content':content,
                             'comments':comments
                             })

        tt = loader.get_template('mls_topic.html')
        return HttpResponse(tt.render(c))

    def post(self,request, topicid,*args, **kwargs):
        result=self.login(request)
        if result['result']=='success':
            return self.get(request,topicid)
        else:
            tt = loader.get_template('mls_login.html')
            c = self.getContext(request,
                            result)
            return HttpResponse(tt.render(c))

    def login(self,request):
        loginForm=LoginForm(request.POST)
        if loginForm.is_valid():
             username = loginForm.cleaned_data['username']
             password = loginForm.cleaned_data['password']
             remember = loginForm.cleaned_data['remember']
             username=username.strip()
             password=password.strip()
             user = authenticate(username=username, password=password)

             if user is not None:
                if user.is_active:  # 登录成功
                    loginLog=UserLoginLog()
                    loginLog.uid=user.id
                    loginLog.src_uuid=username
                    loginLog.login_time=datetime.now()
                    if request.META.has_key('REMOTE_ADDR'):
                        loginLog.ip=request.META['REMOTE_ADDR']
                    elif request.META.has_key('REMOTE_HOST'):
                        loginLog.ip=request.META['REMOTE_HOST']
                    loginLog.src=0
                    loginLog.port=0 #todo
                    loginLog.save()

                    login(request,user)
                    return {'result':'success'}
                else:
                    return {'result':'failed','login_failed':'true'}
             else:
                return {'result':'failed','login_failed':'true'}
        else:
             result={'result':'failed'}

             #result.update(loginForm.errors)
             return result

class MTopicReplyPageView(BaseTopicView):
     '''
     用于单独的回复页面
     '''
     def get(self,request,topicid,replyid,version=None,*args,**kwargs):
        if version=='r':
            url=TopicReply.objects.get(pk=replyid).getReplyUrl()
            return HttpResponseRedirect(url)
        topic=Topic.objects.get(pk=topicid)
        topicReply=TopicReply.objects.get(pk=replyid)

        user=request.user
        if user.is_active:
            try:
                bookmark=BookMark.objects.get(Q(uid__exact=user.id)&Q(tid=topic.id))
            except BookMark.DoesNotExist:
                bookmark=BookMark()
                bookmark.uid=user.id
                bookmark.tid=topic.id

            bookmark.rid=topicReply.id
            bookmark.title1=topic.title
            bookmark.title2=topicReply.title
            bookmark.save()


        c = RequestContext(request,{'page_title':topic.title,'reply':topicReply})
        tt = loader.get_template(version+'ls_topic_reply.html')
        return HttpResponse(tt.render(c))

from ls.models import Comment
from ls.topic_forms import CommentForm
class MTopicComment(BaseTopicView):
    def get(self,request,topicid,replyid=0,result=None,message=None,*args,**kwargs):
        topicid=int(topicid)
        replyid=int(replyid)
        tt = loader.get_template('mls_topic_comment_list.html')
        comments=Comment.objects.filter(topicid__exact=topicid).filter(replyid__exact=replyid).order_by('-created_at')[0:10]
        c = RequestContext(request,{'comments':comments,'topicid':topicid,'replyid':replyid})
        return HttpResponse(tt.render(c))

    def post(self,request,topicid,replyid=0,*args,**kwargs):
        topicid=int(topicid)
        replyid=int(replyid)
        content=request.POST['comment']
        uid=request.user.id
        username=request.user.username
        data={'uid':uid,
              'username':username,
              'content':content,
              'topicid':topicid,
              'replyid':replyid,
              'source_uid':0,}

        comment=CommentForm(data=data)
        if comment.is_valid():
            comment.save()
            return self.get(request,topicid,replyid,result='success')
        else:
            return self.get(request,topicid,replyid,result='failed',message=comment.errors['content'])



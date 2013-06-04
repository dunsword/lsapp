# coding=utf-8

from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from base.base_view import  BaseView
from api.huatan import Huatan
from api.api19 import  ThreadApi
from converter import DocumentConvert


class HtThread:
    pass
class HtSyncView(BaseView):
      def get(self,request,bid=2124418905,*args, **kwargs):
          ht=Huatan()
          bid=int(bid)
          tl = ht.getThreadList(bid)
          boardName =  tl["boardName"]
          boardDesc =  tl["boardDesc"]
          categoryName =  tl["categoryName"]
          cover = tl["cover"]
          threadList = tl['threadList']
          threads=[]
          for item in threadList:
              t=HtThread()
              t.tid=item['tid']
              t.subject=item['subject']
              t.content=item['content']
              t.created_at=item['created_at']
              t.url=item['url']
              threads.append(t)

          c = RequestContext(request,
                            {'boardName':boardName,
                             'boardDesc':boardDesc,
                             'categoryName':categoryName,
                             'threads':threads
                             })

          tt = loader.get_template('sync_htsync.html')
          return HttpResponse(tt.render(c))
class ThreadSyncView(BaseView):
      def get(self,request,tid,page=1,*args, **kwargs):
           tid=int(tid)
           tpa=ThreadApi()
           tp=tpa.getThreadPage(tid,page)

           c = RequestContext(request,{
                                'page':page,
                                'tid':tid,
                                'thread':tp,
                                'posts':tp['posts']

                             })
           convert=DocumentConvert()
           convert.convert(tp)
           convert.converPosts(tp)


           tt = loader.get_template('sync_tsync.html')
           return HttpResponse(tt.render(c))






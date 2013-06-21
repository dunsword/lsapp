# coding=utf-8

from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from base.base_view import  BaseView
from converter import DocumentConvert
from ls.models import Document,TopicReply
from datetime import datetime

from api.docfetcher import DocumentList,DocItem
from api.LouDocFetcherImpl import LouDocFetcher
fecther=LouDocFetcher

class HtThread:
    pass
class HtSyncView(BaseView):
      def get(self,request,bid=2124418905,*args, **kwargs):
          if request.GET.has_key('type'):
              type=request.GET['type']
          else:
              type='board'


          if request.GET.has_key('page'):
              page=int(request.GET['page'])
          else:
              page=1

          if type=='forum':
              fid=int(bid)
              docList=fecther.getLatestDocumentList(sid=fid,size=50,page=page,type='forum')
          elif type=='user':
              uid=int(bid)
              docList=fecther.getLatestDocumentList(sid=uid,size=50,page=page,type='user')
          else:
              bid=int(bid)
              docList=fecther.getLatestDocumentList(bid,30,page=page)
          docs=[]
          for di in docList.doc_list:
             try:
                doc = Document.objects.get_by_source(19,di.tid)
             except Document.DoesNotExist:
                doc = None
             docs.append((di,doc))

          if request.GET.has_key('json'):
             json={}
             docs=[]

             for di in docList.doc_list:
                docs.append({'tid':di.tid,
                             'title':di.subject,
                             'reply_count':di.reply_count,
                             'last_reply_at':di.last_reply_at.strftime('%Y-%m-%d %H:%M:%S')})
             json={'result':'success','page':page,'docs':docs}

             return self._get_json_respones(json)
          else:
            c = RequestContext(request,
                            {
                                'docList':docList,
                                'docs':docs,
                             })

            tt = loader.get_template('sync_htsync.html')
            return HttpResponse(tt.render(c))


class ThreadSyncView(BaseView):


      def get(self,request,tid,page=1,*args, **kwargs):
           tid=int(tid)
           dp=fecther.getDocumentPage(tid,page)
           convert=DocumentConvert()
           totalPage=dp.docItem.reply_count/18+1

           doc=convert.save(dp)

                #
                # c = RequestContext(request,{
                #                 'page':page,
                #                 'tid':tid,
                #                 'dp':dp,
                # })
           #convert=DocumentConvert()
           #convert.convert(tp)
           #convert.converPosts(tp)




           if request.GET.has_key('json'):
               #判断是否需要回复同步
               need_update_reply=doc.source_updated_at<dp.docItem.last_reply_at
               if need_update_reply:
                   for reply in dp.reply_list:
                      tr=convert.saveReply(doc,reply)
                   doc=Document.objects.get(pk=doc.id) #get a new doc obj



               return self._get_json_respones({'result':'success',
                                              'tid':tid,
                                              "page":page,
                                              'reply_count':doc.topic.reply_count,
                                              'source_reply_count':dp.docItem.reply_count,
                                              "totalPage":totalPage,
                                              'need_update_reply':need_update_reply})
           else:
              replys=[]
              for reply in dp.reply_list:
                  try:
                     tr=TopicReply.objects.getBySourceRid(doc.topic.id,reply.rid)
                  except TopicReply.DoesNotExist:
                     tr=None
                  replys.append((reply,tr))
              c=RequestContext(request,{'doc':doc,'dp':dp,'replys':replys,"page":page,'pages':range(1,totalPage)})
              tt = loader.get_template('sync_tsync.html')
              return HttpResponse(tt.render(c))






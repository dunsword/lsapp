# coding=utf-8

from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from base.base_view import  BaseView
from converter import DocumentConvert
from ls.models import Document,TopicReply

from api.docfetcher import LouDocFetcher,DocumentList,DocItem
fecther=LouDocFetcher

class HtThread:
    pass
class HtSyncView(BaseView):
      def get(self,request,bid=2124418905,*args, **kwargs):

          bid=int(bid)
          docList=fecther.getLatestDocumentList(bid,30)
          docs=[]
          for d in docList.doc_list:
             try:
                doc = Document.objects.get_by_source(19,d.tid)
             except Document.DoesNotExist:
                doc = None
             docs.append((d,doc))
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
              for reply in dp.reply_list:
                 tr=convert.saveReply(doc,reply)
              doc=Document.objects.get(pk=doc.id) #get a new doc obj

              return self._get_json_respones({'result':'success',
                                              'tid':tid,
                                              "page":page,
                                              'reply_count':doc.topic.reply_count,
                                              'source_reply_count':dp.docItem.reply_count,
                                              "pages":range(1,totalPage)})
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






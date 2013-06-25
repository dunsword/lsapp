# coding=utf-8

from django.template import loader
from django.http import HttpResponse
from django.template import RequestContext
from base.base_view import BaseView
from ls.models import Document, TopicReply
from api.HongXiuFetcherImpl import HXDocumentFetcher
from sync.converter import DocumentConvert

fetcher = HXDocumentFetcher
siteId = 2


class HxSyncView(BaseView):
    def get(self, request, tid=0, *args, **kwargs):
        cid = 'zl1_8'
        if request.GET.has_key('type'):
            cid = request.GET['type']

        if request.GET.has_key('page'):
            page = int(request.GET['page'])
            if page <= 0:
                page = 1
        else:
            page = 1

        if tid > 0:
            docList = fetcher.getDocumentDetailByTid(tid=tid)
        else:
            docList = fetcher.getLatestDocumentList(sid=cid, size=page)

        docs = []
        for di in docList.doc_list:
            try:
                doc = Document.objects.get_by_source(siteId, di.tid)
            except Document.DoesNotExist:
                doc = None
            docs.append((di, doc))

        if request.GET.has_key('json'):
            docs = []

            for di in docList.doc_list:
                docs.append({'tid': di.tid,
                             'title': di.subject,
                             # 'view_count': di.view_count,
                             'reply_count': di.reply_count,
                             'last_reply_at': di.last_reply_at.strftime('%Y-%m-%d %H:%M:%S')})
            json = {'result': 'success', 'page': page, 'docs': docs}

            return self._get_json_respones(json)
        else:
            c = RequestContext(request,
                               {
                                   'docList': docList,
                                   'docs': docs,
                               })

            tt = loader.get_template('sync_hxsync.html')
            return HttpResponse(tt.render(c))


class HxThreadSyncView(BaseView):
    def get(self, request, tid, page=1, *args, **kwargs):
        tid = int(tid)
        dp = fetcher.getDocumentPage(tid, page)
        convert = DocumentConvert()
        totalPage = dp.docItem.reply_count

        doc = convert.save(dp, siteId=2)

        if request.GET.has_key('json'):
            #判断是否需要回复同步
            need_update_reply = doc.source_updated_at < dp.docItem.last_reply_at
            if need_update_reply:
                for reply in dp.reply_list:
                    tr = convert.saveReply(doc, reply)
                doc = Document.objects.get(pk=doc.id) #get a new doc obj

            return self._get_json_respones({'result': 'success',
                                            'tid': tid,
                                            "page": page,
                                            'reply_count': doc.topic.reply_count,
                                            'source_reply_count': dp.docItem.reply_count,
                                            "totalPage": totalPage,
                                            'need_update_reply': need_update_reply})
        else:
            replys = []
            for reply in dp.reply_list:
                try:
                    tr = TopicReply.objects.getBySourceRid(doc.topic.id, reply.rid)
                except TopicReply.DoesNotExist:
                    tr = None
                replys.append((reply, tr))
            c = RequestContext(request,
                               {'doc': doc, 'dp': dp, 'replys': replys, "page": page, 'pages': range(1, totalPage)})
            tt = loader.get_template('sync_tsync.html')
            return HttpResponse(tt.render(c))




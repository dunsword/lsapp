# coding=utf-8

import re

from django.template import loader
from django.http import HttpResponse
from django.template import RequestContext
from api.QiDianFetcherImpl import QDDocumentFetcher
from base.base_view import BaseView, PageInfo
from cron.spider.getAvatar import WebPageContent
from ls.models import Document, TopicReply
from sync.converter import DocumentConvert

fetcher = QDDocumentFetcher
siteId = 1


class QDSyncView(BaseView):
    def get(self, request, tid=0, *args, **kwargs):
        cid = '22'
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
                                   'pageInfo': PageInfo(page, 30 * 100, 100, u"/sync/qdsync?type=%s&page=" % cid),
                               })

            tt = loader.get_template('sync_qdsync.html')
            return HttpResponse(tt.render(c))


class QDThreadSyncView(BaseView):
    def get(self, request, tid, page=1, *args, **kwargs):
        tid = int(tid)
        dp = fetcher.getDocumentPage(tid, page)
        convert = DocumentConvert()
        totalPage = dp.docItem.reply_count

        doc = convert.save(dp, siteId=siteId)

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


class QDIndexSyncView(BaseView):
    def get(self, request):
        c = RequestContext(request, {})
        tt = loader.get_template('sync_qdsync_index.html')
        return HttpResponse(tt.render(c))


class QDSyncHotData:
    def __init__(self):
        self.tid = 0
        self.name = 0


TopWeek = {
    "http://script.qidian.com/Script/BookChannel1ThirdScript.js": "奇幻",
    "http://script.qidian.com/Script/BookChannel2ThirdScript.js": "武侠",
    "http://script.qidian.com/Script/BookChannel4ThirdScript.js": "都市",
    # "http://script.qidian.com/Script/BookChannel5ThirdScript.js":"",
    "http://script.qidian.com/Script/BookChannel6ThirdScript.js": "军事",
    # "http://script.qidian.com/Script/BookChannel7ThirdScript.js":"",
    # "http://script.qidian.com/Script/BookChannel8ThirdScript.js":"",
    "http://script.qidian.com/Script/BookChannel9ThirdScript.js": "科幻",
    # "http://script.qidian.com/Script/BookChannel10ThirdScript.js":"",
    "http://script.qidian.com/Script/BookChannel15ThirdScript.js": "青春",
    "http://script.qidian.com/Script/BookChannel21ThirdScript.js": "玄幻",
    "http://script.qidian.com/Script/BookChannel22ThirdScript.js": "仙侠",
}


class QDSyncHotView(BaseView):
    def get(self, request):
        topWeekList = []
        for key in TopWeek:
            url = key
            category = TopWeek[key]
            content = WebPageContent(url)
            subTitle = u'var TopWeekClickVip=['
            data = content.getData().decode('utf-8')
            start = data.index(subTitle)
            end = data.index("];", start)
            if start <= 0 or end <= 0:
                continue
            data = data[start + len(subTitle):end - 1]
            objectPattern = re.compile(r'new Book')
            al = objectPattern.split(data)
            for a in al:
                a = a.strip(',').strip()
                if a:
                    a = a[1:len(a) - 1]
                    data = a.split(',')
                    topWeekBook = QDSyncHotData()
                    topWeekList.append(topWeekBook)
                    topWeekBook.tid = data[0].strip('\'')
                    topWeekBook.name = "%s[%s]" % (data[1].strip('\''), category)
        c = RequestContext(request,
                           {
                               'topWeekList': topWeekList,
                           })

        tt = loader.get_template('sync_qdsync_top.html')
        return HttpResponse(tt.render(c))

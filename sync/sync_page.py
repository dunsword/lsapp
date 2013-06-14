# coding=utf-8
from sync.converter import DocumentConvert
from ls.models import Document, TopicReply

from api.docfetcher import DocumentList, DocItem
from api.LouDocFetcherImpl import LouDocFetcher
import time
import logging
log=logging.getLogger('info')
fecther = LouDocFetcher
convert = DocumentConvert()


def syncThread(tid):
    try:
        try:
            doc = Document.objects.get_by_source(19, tid)
        except Document.DoesNotExist:
            doc = None

        dp = fecther.getDocumentPage(tid, 1)
        d=dp.docItem
        totalPage = d.reply_count / 18 + 1
        log.log(logging.INFO,u'同步帖子' + unicode(tid) + u'.....')
        log.log(logging.INFO,u'共' + unicode(totalPage) + u'页')
        log.log(logging.INFO,u'帖子标题:' + d.subject)

        for n in range(1, totalPage):
            try:
                dp = fecther.getDocumentPage(tid, n)
                if n == 1:
                    doc = convert.save(dp)
                    log.log(logging.INFO,u'帖子' + unicode(tid) + u'已经保存')
                for reply in dp.reply_list:
                    tr = convert.saveReply(doc, reply)
                log.log(logging.INFO,u'帖子' + unicode(tid) + u'第' + unicode(n) + u'页回复已经保存')
            except Exception, e:
                print e
        return doc
    except Exception, e:
                print e

def sycnThreadList(page):
    log.log(logging.INFO,u'start sync page:'+str(page))
    try:
        docList = fecther.getLatestDocumentList(sid=26, size=50, page=page, type='forum')
        docs = []
        for d in docList.doc_list:
            try:
                try:
                    doc = Document.objects.get_by_source(19, d.tid)
                except Document.DoesNotExist:
                    doc = None

                tid = d.tid
                totalPage = d.reply_count / 18 + 1
                log.log(logging.INFO,u'同步帖子' + unicode(tid) + u'.....')
                log.log(logging.INFO,u'共' + unicode(totalPage) + u'页')
                log.log(logging.INFO,u'帖子标题:' + d.subject)

                for n in range(1, totalPage):
                    time.sleep(2)
                    try:
                        dp = fecther.getDocumentPage(tid, n)
                        if n == 1:
                            doc = convert.save(dp)
                            log.log(logging.INFO,u'帖子' + unicode(tid) + u'已经保存')
                        for reply in dp.reply_list:
                            tr = convert.saveReply(doc, reply)
                        log.log(logging.INFO,u'帖子' + unicode(tid) + u'第' + unicode(n) + u'页回复已经保存')
                    except Exception, e:
                        print e
            except Exception, e:
                print e
    except Exception, e:
        print e

    log.log(logging.INFO,u'-------------------------------')


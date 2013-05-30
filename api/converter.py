# coding=utf-8
__author__ = 'paul'

from api19 import ThreadApi
from ls.models import Document,Topic

UID=777
UNAME=u'一缕红尘'

class DocumentConvert:
    def convert(self,threadPage):
        tid=threadPage['tid']
        fid=threadPage['fid']
        subject=threadPage['subject']
        viewCount=threadPage['viewCount']
        replyCount=threadPage['replyCount']
        currentPage=threadPage['currentPage']
        authorid=threadPage['posts'][0]['uid']
        content=threadPage['posts'][0]['msg']
        try:
            doc=Document.objects.get(source_tid__exact=tid)
        except Document.DoesNotExist:
            doc=Document.objects.create_document(777,UNAME,subject,content,19,'',104,'未知')

        return doc


def test(tid=4891369839152366):
    ta=ThreadApi()
    dc=DocumentConvert()

    tp=ta.getThreadPage(tid)
    doc=dc.convert(tp)
    print doc





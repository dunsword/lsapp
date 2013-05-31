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
        url=threadPage['url']
        try:
            doc=Document.objects.get(source_tid__exact=tid)
        except Document.DoesNotExist:
            doc=Document.objects.create_document(
                userid=777,
                username=UNAME,
                title=subject,
                content=content,
                read_count=viewCount,
                reply_count=0,
                source_id=19,
                source_url=url,
                categoryid=104,
                author_name=u'未知',
                )

        return doc


def test(tid=4891369839152366):
    ta=ThreadApi()
    dc=DocumentConvert()

    tp=ta.getThreadPage(tid)
    doc=dc.convert(tp)
    print doc





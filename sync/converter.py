# coding=utf-8
__author__ = 'paul'

from api.api19 import ThreadApi
from ls.models import Document,Topic,TopicReply

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
        authorid=threadPage['uid']
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
                source_tid=tid,
                categoryid=104,
                author_name=u'未知',
                source_uid=authorid
                )
        return doc

    def converPosts(self,threadPage):
        tid=threadPage['tid']
        doc=Document.objects.get(source_tid__exact=tid)
        fid=threadPage['fid']
        posts=threadPage['posts']
        for post in posts:
            if post['is_first']:
                continue
            pid=long(post['pid'])
            q=TopicReply.objects.filter(topicid__exact=doc.topic.id).filter(source_pid__exact=pid)
            if len(list(q))==0: #同步
                if threadPage['uid']==post['uid']:
                    isChapter=True
                else:
                    isChapter=False
                tr=TopicReply(userid=UID,
                              username=UNAME,
                              topicid=doc.topic.id,
                              title=post['title'],
                              content=post['msg'],
                              is_chapter=isChapter,
                              source_url=doc.source_url, #接口无法获取页码，先不实现。用帖子页地址代替
                              source_pid=pid)
                tr.save()


def test(tid=4891369839152366):
    ta=ThreadApi()
    dc=DocumentConvert()

    tp=ta.getThreadPage(tid)
    doc=dc.convert(tp)

    print doc





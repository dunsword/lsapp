# coding=utf-8
__author__ = 'paul'


from api.LouDocFetcherImpl import LouDocFetcher,LouCategory
from ls.models import Document,Topic,TopicReply,Comment
from api.docfetcher import DocItemDetailPage,RelyItem,DocItem,SourceInfo,RateItem


#TODO user get user random api
UID=777
UNAME=u'一缕红尘'

class DocumentConvert:
    def saveRate(self,doc,reply,topicReply=None):
        '''
            保持指定回复的评分

        :param doc: Document对象
        :param reply: ReplyItem对象
        :param topicReply: TopicReply对象，如果为None，Comment的rid记为0，即作为主帖的评论
        '''
        rid=0;
        if topicReply is not None:
            rid=topicReply.id
        if reply.rates is not None:
                rates=reply.rates
                for rate in rates:
                    if len(rate.content)<2:
                        continue
                    if rate.content == u'祝福……':
                        continue
                    if rate.content.__contains__(u'来自'):
                        continue
                    #rate=RateItem()
                    try:
                        comment=Comment.objects.get(source_id__exact=long(rate.rate_id))
                    except Comment.DoesNotExist:

                        comment=Comment()
                        comment.topicid=doc.topic.id
                        comment.replyid=rid
                        comment.uid=0
                        comment.source_uid=long(rate.uid)
                        comment.username=rate.username
                        comment.source_id=long(rate.rate_id)
                        comment.content=rate.content
                        comment.created_at=rate.created_at
                        comment.save()

    def saveReply(self,doc,reply):
        if reply.is_first:
            self.saveRate(doc,reply)
            return None

        if reply.uid==doc.source_uid:
            is_chapter=True
        else:
            is_chapter=False
        try:
            tr=TopicReply.objects.getBySourceRid(doc.topic.id,reply.rid) #filter(topicid__exact=doc.topic.id).filter(source_pid__exact=reply.rid)
            tr.content=reply.content
            tr.title=reply.subject
            tr.is_chapter=is_chapter
            tr.save()
        except TopicReply.DoesNotExist:
            if not reply.is_first:
                source_url = doc.source_url
                if reply.reply_url:
                    source_url = reply.reply_url
                tr=TopicReply.objects.createReply(topicid=doc.topic.id,
                                       userid=UID,
                                       username=UNAME,
                                       title=reply.subject,
                                       content=reply.content,
                                       is_chapter=is_chapter,
                                       source_pid=reply.rid,
                                       source_url=source_url,
                                       created_at=reply.created_at)
                self.saveRate(doc,reply,tr)

            if doc.source_updated_at<tr.created_at:
                doc.source_updated_at=tr.created_at
                doc.save()



        return tr

    def save(self,docPage,siteId=19):
        u'''
        根据接口获取到的内容，保存主帖信息。如果doc对象当前不存在，创建并保存。
        如果已经存在，更新uid、siteid、封面的信息（主要考虑到以前同步的数据未包含这些信息，以后可以不更新）
        另外还还更新对应topic的read_count,content

        注：不更新source_updated_at,用于检查是否需要同步回复，回复同步时更新
        '''

        di=docPage.docItem
        try:
            doc=Document.objects.get_by_source(siteId,docPage.docItem.tid)

        except Document.DoesNotExist:
            doc=Document.objects.create_document(userid=UID,
                                                 username=UNAME,
                                                 title=di.subject,
                                                 content=di.content,
                                                 source_id=di.siteid,
                                                 source_tid=di.tid,
                                                 source_url=di.url,
                                                 source_uid=di.uid,
                                                 read_count=di.view_count,
                                                 reply_count=0,
                                                 author_name=u'未知',
                                                 source_updated_at=di.created_at,
                                                 categoryid=2
                                                 )


        if docPage.page_number==1:
            doc.source_uid=di.uid
            doc.source_url=di.url
            doc.source_id=di.siteid
            doc.source_cover_img=di.cover_img
            doc.save()
            doc.topic.created_at=di.created_at
            doc.topic.content=di.content
            doc.topic.read_count=di.view_count
            #doc.topic.content=di.content
            tags=LouCategory.getCategoryByTags(di.tags)
            if len(tags)>0:
                doc.topic.categoryid=tags[0]
            if len(tags)>1:
                doc.topic.catid1=tags[1]
            if len(tags)>2:
                doc.topic.catid2=tags[2]
            doc.topic.save()
        return doc

    def convert(self,threadPage,siteId=19):
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
                source_id=siteId,
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
    # ta=ThreadApi()
    # dc=DocumentConvert()
    #
    # tp=ta.getThreadPage(tid)
    # doc=dc.convert(tp)
    #
    # print doc
    pass




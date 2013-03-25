# coding=utf-8
from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    status=models.IntegerField('status',choices=[(1,"正常"),(2,"删除"),(3,"隐藏")],default=1,db_index=True)
    created_at=models.DateTimeField('created time', default=timezone.now,db_index=True)
    updated_at=models.DateTimeField('updated time', default=timezone.now,db_index=True)
    class Meta:
        abstract=True


class SiteSource(BaseModel):
    name=models.CharField('site name',max_length=256)
    homepage=models.URLField('site home page')
    desc=models.CharField('description',max_length=2048)


class Topic(BaseModel):
    TOPIC_TYPE_NORMAL=1
    TOPIC_TYPE_DOCUMENT=2
    TOPIC_TYPE_VIDEO=3
    TOPIC_TYPE_SHOP=4
    
    userid=models.IntegerField('user id')
    username=models.CharField('user name',max_length=30)
    title=models.CharField('topic title',max_length=255)
    content=models.CharField('topic content',max_length=2048)
    categoryid=models.IntegerField('category id',default=1)
    like_count=models.IntegerField('like count',default=0)
    read_count=models.IntegerField('read count',default=0)
    reply_count=models.IntegerField('reply count',default=0)
    topic_type=models.IntegerField('topic type',choices=[(1,"普通"),(2,"小说"),(3,"视频"),(4,"购物")],default=1,db_index=True)
    
    def getDocument(self):
        if self.topic_type==2:
            return Document.objects.get(topic__exact=self)
        return None

class DocumentManager(models.Manager):
    def create_document(self,userid,title,content,source_id,source_url,categoryid):
        topic=Topic.objects.create(userid=userid,title=title,content=content,categoryid=categoryid,topic_type=Topic.TOPIC_TYPE_DOCUMENT)
        doc=Document.objects.create(source_id=source_id,source_url=source_url,topic=topic)
        doc.save()
        return doc
    
class Document(models.Model):
    objects=DocumentManager()
    author_name=models.CharField('author name',max_length=256,null=True,default=None)
    update_status=models.SmallIntegerField('status',default=0)
    source_id=models.IntegerField('sourse id')
    source_url=models.URLField('source url')
    topic=models.OneToOneField(Topic,related_name='ref+')

class Feed(BaseModel):
#    FEED_TYPE_RECOMMEND=1
#    FEED_TYPE_UPDATE=2
#    FEED_TYPE_CATEGORY_HOT=3
#    
#    type={
#          Feed.FEED_TYPE_RECOMMEND:'推荐',
#          Feed.FEED_TYPE_UPDATE:'更新',
#          Feed.FEED_TYPE_CATEGORY_HOT:'热门',
#          }
    
    userid=models.IntegerField('user id')
    username=models.CharField('user name',max_length=30)
    docid=models.IntegerField('doc id')
    feed_type=models.SmallIntegerField('feed type',default=1)

class Category(BaseModel):
    name=models.CharField('category name',max_length=100)

class TopicReply(BaseModel):
    userid=models.IntegerField('user id')
    username=models.CharField('user name',max_length=30)
    topicid=models.IntegerField('topic id',db_index=True)
    title=models.CharField('topic title',max_length=255,default="")
    content=models.CharField('topic content',max_length=2048)
    
 
# coding=utf-8
from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    created_at=models.DateTimeField('created time', default=timezone.now)
    updated_at=models.DateTimeField('updated time', default=timezone.now)
    class Meta:
        abstract=True

class SiteSource(BaseModel):
    name=models.CharField('site name',max_length=256)
    homepage=models.URLField('site home page')
    desc=models.CharField('description',max_length=2048)
    
    
class Document(models.Model):
    author_name=models.CharField('author name',max_length=256,null=True,default=None)
    title=models.CharField('bookname',max_length=256)
    content=models.CharField('content',max_length=1024)
    created_at=models.DateTimeField('created time', default=timezone.now)
    updated_at=models.DateTimeField('updated time', default=timezone.now)
    read_count=models.IntegerField('read count',default=0)
    like_count=models.IntegerField('like count',default=0)
    reply_count=models.IntegerField('reply count',default=0)
    update_status=models.SmallIntegerField('status',default=0)
    categoryid=models.IntegerField('category id')
    source_id=models.IntegerField('sourse id')
    source_url=models.URLField('source url')

class Feed(models.Model):
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
    created_at=models.DateTimeField('created time',default=timezone.now)
    feed_type=models.SmallIntegerField('feed type',default=1)

class Category(models.Model):
    name=models.CharField('category name',max_length=100)
    
    
class Topic(models.Model):
    userid=models.IntegerField('user id')
    username=models.CharField('user name',max_length=30)
    title=models.CharField('topic title',max_length=255)
    content=models.CharField('topic content',max_length=2048)
    categoryid=models.IntegerField('category id',default=1)
    read_count=models.IntegerField('read count',default=0)
    reply_count=models.IntegerField('reply count',default=0)
    created_at=models.DateTimeField('created time',default=timezone.now)
    updated_at=models.DateTimeField('updated time',default=timezone.now)

class TopicReply(models.Model):
    userid=models.IntegerField('user id')
    username=models.CharField('user name',max_length=30)
    topicid=models.IntegerField('topic id',db_index=True)
    title=models.CharField('topic title',max_length=255)
    content=models.CharField('topic content',max_length=2048)
    created_at=models.DateTimeField('created time',default=timezone.now)
    updated_at=models.DateTimeField('updated time',default=timezone.now)
 